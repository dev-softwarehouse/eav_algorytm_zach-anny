#ifndef __DECISION_RULE__
#define __DECISION_RULE__

#include <iostream>
#include <vector>
#include <tuple>
#include <map>
#include <utility>
#include <fstream>
#include <string>
#include <algorithm>
#include <set>
#include <sstream>

#include "Utils.h"

using namespace std;

class DecisionRules
{
public:
    void loadDecisionTablePath(const string& fileLoc);
    void loadBestAttributesPath(const string& fileLoc);
    void generateDecisionRules(bool forceGenerate = false);
    void displayDecisionRules();
    void displayRuleSupport();

private:
    map<string, vector<int>> columnValue;
    vector<string> bestAttributes;
    set<string> rules;
    vector<vector<int>> ruleSupport;
    int minSupport;
    int maxSupport;
};

#endif