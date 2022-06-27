from signal import raise_signal
from django.shortcuts import render
from django.db import transaction, connection
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser,FileUploadParser,FormParser
from rest_framework.views import APIView
from django.shortcuts import render
from openpyxl import load_workbook
from .generate_rules import generate_rules
import pandas as pd
from .models import Eva,decisionValue
from .serializers import FileSerializer
from .utils.create_eav import create_eav,set_decision_values
from io import BytesIO
# Create your views here.


class fileInputView(APIView):
    parser_classes = (MultiPartParser, FormParser,)
    @transaction.atomic
    @swagger_auto_schema(request_body=FileSerializer(),tags = ['DecisionRules'])
    def post(self, request):
        try:
            file = request.FILES.get("file", None)
            file_name = file.name
            file_obj = request.FILES.get("file", None).read()
            data = None
            dataframe = pd.read_excel(BytesIO(file_obj))
            Attributes = (dataframe.columns).tolist()
        except Exception as e:
            raise Response({'error':'Invalid File'})
        
        create_eav(dataframe)
        set_decision_values()
        f = open("decision_table.txt", "w")
        for col in dataframe.columns:
            f.write(str(col))
            for value in dataframe[col].values:
                f.write(" "+str(value))
            f.write('\n')    
        f.close()
        # eva = Eva.objects.all()
        # values = set(eva.values_list('value',flat=True))
        # decisionValue.objects.all().delete()
        # for value in values:
        #     decisionValue.objects.create(value=value)
        rules_list = [] 
        num_of_rows = len(dataframe.index)
        col_index = 0
        cursor = connection.cursor()    
        cursor.execute("SELECT attribute , STDDEV( average_value ) AS quality FROM ( SELECT e.attribute , e.decision , AVG( v.id ) AS average_value FROM decisionrules_eva e JOIN decisionrules_decisionvalue v ON e.value = v.value GROUP BY attribute , decision ) attribute_average_values GROUP BY attribute ORDER BY quality DESC")
        row = cursor.fetchall()
        print("row info")
        print(list(row))
        p = 2
        p -= 1
        attr = []
        f = open("ranking_of_Attributes.txt", "w")
        for col in row:
            if p == -1:
                break
            attr.append(col[0])
            f.write(col[0]+" ")
            p-=1
        f.write('d')
        attr.append('d')
        
        print("best attri")
        print(attr)
        print(dataframe[attr])
        bestdataframe = dataframe[attr]
        print(attr)
        rules = []
        print(bestdataframe)
        for index in (bestdataframe.index):
            data = bestdataframe.iloc[index]
            subdata = None
            for ind,col in enumerate(attr):
                if col != 'd':
                    if ind==0:
                        subdata = bestdataframe.loc[bestdataframe[col] == data[ind]]
                    else:
                        subdata = subdata.loc[subdata[col] == data[ind]]
                       
                    if  not len(set(subdata['d']))== 1: # not degenerate
                        continue 
                    rules_list.append((subdata.iloc[0].values).tolist())
                    rules.append(subdata)   
        
        # d_list is for decsion list
        d_list = dataframe['d'].values
        min_rule = min(d_list)
        max_rule = max(d_list)
        num_of_rows = len(dataframe.index)
        rule_length = {
            'min_rule_length':min_rule,
            'max_rule_length':max_rule,    
        }
        
        rule_uniqueness = set(map(tuple, rules_list))
        rules1 = generate_rules(rules,attr)
        return Response({"attributes":Attributes,"rules1":rules1,"rules":rules_list,'number_of_rows':num_of_rows,"file_name":file_name,"rule_length":rule_length,"rule_uniqueness":rule_uniqueness})


