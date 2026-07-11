#import "devmode.h"
BOOL checkDeveloperMode(void) { return YES; }
BOOL armDeveloperMode(BOOL* enabled) { if(enabled) *enabled=YES; return YES; }