#include "../include/DecisionRules.h"

void DecisionRules::loadDecisionTablePath(const string& fileLoc)
{
    ifstream decisionTableFile(fileLoc);
    vector<int> values;
    string number;
    string column;
    columnValue.clear();
    while (decisionTableFile >> number)
    {
        if (!Utils::isNumber(number))
        {
            column = number;
            vector<int> values;
            columnValue[column] = values;
        }

        if (Utils::isNumber(number))
        {
            int num = stoi(number);
            columnValue[column].push_back(num);
        }
    }
    decisionTableFile.close();
}

void DecisionRules::loadBestAttributesPath(const string& fileLoc)
{
    ifstream bestAtttributesFile(fileLoc);
    string attributes;
    bestAttributes.clear();
    while (bestAtttributesFile >> attributes)
    {
        bestAttributes.push_back(attributes);
    }
    bestAtttributesFile.close();
}

void DecisionRules::generateDecisionRules(bool forceGenerate)
{
    if ( forceGenerate || rules.empty() )
    {
        rules.clear();
        ruleSupport.clear();
        if ( columnValue.size() > 0 && bestAttributes.size() > 0 )
        {
            unsigned int szAtt = columnValue[bestAttributes[0]].size();
            for (unsigned int index = 0; index < szAtt ; index++) // access columns values
            {
                int checkValue;
                vector<int> checkRuleIndex;
                unsigned int sz1 = bestAttributes.size();
                for (unsigned int attr_index = 0; attr_index < sz1 - 1; attr_index++) // get best attributes
                {
                    vector<int> decisionValue;
                    checkValue = columnValue[bestAttributes[attr_index]][index];
                    if (attr_index == 0)
                    {
                        // get column value for decision comparision
                        unsigned int sz = columnValue[bestAttributes[0]].size();
                        for (unsigned int val_index = 0; val_index < sz; val_index++) // accessing best attributes values for checking
                        {

                            if (columnValue[bestAttributes[attr_index]][val_index] == checkValue) // check if col value is available in another decision table's row
                            {
                                checkRuleIndex.push_back(val_index); // push index of that columns
                            }
                        }
                    }

                    if (attr_index > 0)
                    {
                        vector<int> tempDecsion;
                        tempDecsion = checkRuleIndex;
                        checkRuleIndex.clear();
                        // get column value for decision comparision
                        unsigned int sz = tempDecsion.size();
                        for (unsigned int decision_index = 0; decision_index < sz; decision_index++) //  for degenerate
                        {
                            if (columnValue[bestAttributes[attr_index]][tempDecsion[decision_index]] == checkValue)
                            {
                                checkRuleIndex.push_back(tempDecsion[decision_index]);
                            }
                        }
                    }

                    unsigned int sz = checkRuleIndex.size();
                    for (unsigned int decision_index = 0; decision_index < sz; decision_index++) //  for degenerate
                    {
                        decisionValue.push_back(columnValue["d"][checkRuleIndex[decision_index]]);
                    }

                    if (!Utils::allEqual(decisionValue))

                    {
                        continue;
                    }

                    for (unsigned int decision_index = 0; decision_index < checkRuleIndex.size(); decision_index++) //  for degenerate
                    {
                        vector<int> temRuleSupport;
                        if (columnValue[bestAttributes[attr_index]][checkRuleIndex[decision_index]] == checkValue)
                        {
                            stringstream rule;
                            for (unsigned int rule_index = 0; rule_index < sz1; rule_index++)
                            {
                                temRuleSupport.push_back(columnValue[bestAttributes[rule_index]][checkRuleIndex[decision_index]]);
                                rule << bestAttributes[rule_index] << " " << columnValue[bestAttributes[rule_index]][checkRuleIndex[decision_index]] << " ";
                            }
                            ruleSupport.push_back(temRuleSupport);
                            string rule_s = rule.str();
                            rules.insert(rule_s);       //only push unique rules
                        }

                        decisionValue.push_back(columnValue[bestAttributes[attr_index]][checkRuleIndex[decision_index]]);
                    }
                }
            }
        }
    }
}

void  DecisionRules::displayDecisionRules()
{
    set<string>::iterator rulesItr;
    for (rulesItr = this->rules.begin(); rulesItr != this->rules.end(); rulesItr++)
    {
        cout << *rulesItr << endl;
    }
    cout << endl;

}



void DecisionRules::displayRuleSupport()
{

   sort( ruleSupport.begin(), ruleSupport.end() );
   ruleSupport.erase(std::unique(ruleSupport.begin(), ruleSupport.end()), ruleSupport.end());
   {
    int d;
    minSupport = 0;
    maxSupport = 0;
    for(auto row_obj : ruleSupport)
    {
        d = row_obj[row_obj.size()-1];
        for(auto row_obj2 : ruleSupport){
            vector<int> ruleUpdate;
            if (d == row_obj2[row_obj2.size()-1]){
                if ((row_obj[0] == row_obj2[0]) and (row_obj[1] != row_obj2[1])){
                    // rule << bestAttributes[0] << " " << row_obj[0] << " " << " " << d;
                    minSupport = 1;
                    break;
                }
                else if ((row_obj[0] != row_obj2[0]) and (row_obj[1] == row_obj2[1])){
                    // rule << bestAttributes[1] << " " << row_obj[1] << " " << " " << d;
                    minSupport = 1;
                    break;
                }
                else {
                    if (minSupport == 0){
                       minSupport = 2;
                    }
                    //  rule << bestAttributes[0] << " " << row_obj[0] << bestAttributes[1] << " " << row_obj[1]  << " " << " " << 'd' << d;
                }
            }
            if (maxSupport < d){
            maxSupport = d;
        }
        }
    }
}
    cout<<"minSupport"<<minSupport<<endl;
    cout<<"maxSupport"<<maxSupport<<endl;

}

