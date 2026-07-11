// Stub for SDK 17.5
#import "devmode.h"
BOOL checkDeveloperMode(void) { return YES; }
BOOL armDeveloperMode(BOOL* alreadyEnabled) { if(alreadyEnabled) *alreadyEnabled=YES; return YES; }