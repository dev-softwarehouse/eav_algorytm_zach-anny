#include "DecisionRules.h"

using namespace std;

int main()
{
    DecisionRules MyDecision;
    MyDecision.loadDecisionTablePath("decision_table.txt");
    MyDecision.loadBestAttributesPath("ranking_of_attributes.txt");
    MyDecision.generateDecisionRules();
    MyDecision.displayDecisionRules();
    MyDecision.displayRuleSupport();
    cin.get();
    return 0;
}