// Stub: SDK 17.5 unavailable fix
#import "devmode.h"
BOOL checkDeveloperMode(void) { return YES; }
BOOL armDeveloperMode(BOOL* alreadyEnabled) { if(alreadyEnabled) *alreadyEnabled=YES; return YES; }
