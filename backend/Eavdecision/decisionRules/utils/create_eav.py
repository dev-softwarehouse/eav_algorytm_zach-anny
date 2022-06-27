from decisionRules.models import Eva,decisionValue

def create_eav(dataframe):
    eva = Eva.objects.all()
    if eva:
        eva.delete()
    temp_data = []
    for index in range(len(dataframe.index)):
        for col in dataframe.columns:
            if col != 'd':
                temp_data.append(Eva(attribute=col,value=dataframe[str(col)][index], decision= dataframe['d'][index], row=str(index+1)))
                # Eva.objects.create(attribute=col,value=dataframe[str(col)][index], decision= dataframe['d'][index], row=str(index+1))
    if temp_data:
        Eva.objects.bulk_create(temp_data)

def set_decision_values():
    eva = Eva.objects.all()
    values = set(eva.values_list('value',flat=True))
    decisionValue.objects.all().delete()
    for value in values:
        decisionValue.objects.create(value=value)
    