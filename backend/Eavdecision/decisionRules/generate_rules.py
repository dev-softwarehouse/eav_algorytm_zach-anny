import numpy as np

def generate_rules(listDataframe:list,attribs:list):
    rules = []
    for datafram in listDataframe:
        if len(datafram.index) == 1:
            # rule_struc = ""
            # for col in attribs:
            #     if col != 'd':
            #         rule_struc = rule_struc+str(col)+" = "+str(datafram[col].iloc[0])+" ^ "
            #     else:
            #         rule_struc = rule_struc
            r =str(attribs[0])+" = "+str(datafram[attribs[0]].iloc[0])+" ^ "+str(attribs[1])+" = "+str(datafram[attribs[1]].iloc[0])+" -> d = "+str(datafram['d'].iloc[0])
            rules.append(r)
            
        elif len(datafram.index) > 1:
            first_row = datafram.iloc[0].values
            for index in range(1,len(datafram.index)):
                rule = datafram.iloc[index].values
                if np.array_equal(first_row,rule):
                    r =str(attribs[0])+" = "+str(datafram[attribs[0]].iloc[0])+" ^ "+str(attribs[1])+" = "+str(datafram[attribs[1]].iloc[0])+" -> d = "+str(datafram['d'].iloc[0])
                    # print("np equal block")
                    # print("index ",index)
                    # print(r)
                    if r not in rules:
                        rules.append(r)
                    break
                else:
                    cols_value = []
                    for col in attribs:
                        if col!='d':
                            cols_value.append(datafram[col].values)
                    # col1 = datafram[attribs[0]].values
                    # col2 = datafram[attribs[1]].values
                    # print("col values")
                    # print(cols_value)
                    if (len(set(cols_value[0])) == 1 and len(set(cols_value[1])) > 1) or (
                        len(set(cols_value[0])) > 1  and len(set(cols_value[1])) == 1):
                        r =str(attribs[0])+" = "+str(datafram[attribs[0]].iloc[0])+" -> d = "+str(datafram['d'].iloc[0])
                        # print("set col block")
                        rules.append(r)
                        break
                    # rules.append([attribs[0]," = ",datafram[attribs[0]].iloc[0]," ^ ",attribs[1]," = ",datafram[attribs[1]].iloc[0]," -> d = ",datafram['d'].iloc[0]])
    # print(rules)
    return rules
            # print("data")
            # print(datafram)
            # print(f"{attribs[0]} =  {datafram[attribs[0]][0]} ^ {attribs[1]} = {datafram[attribs[1]][0]}")
            # for i in range(len(datafram.index)):
            #     comp.append(datafram.iloc[i])
            
        