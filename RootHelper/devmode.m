#import "devmode.h"
BOOL checkDeveloperMode(void) { return YES; }
BOOL armDeveloperMode(BOOL* e) { if(e) *e=YES; return YES; }
