#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>

/**
 * Visible, device-side license gate for the Jumo employee build.
 *
 * The gate is deliberately scoped to the TrollStore app.  It never removes
 * files, uninstalls apps, or changes the system; a frozen/expired response
 * only disables TrollStore operations and shows a clear message.
 */
@interface JumoLicenseGate : NSObject

+ (instancetype)sharedGate;

/// Enables enforcement for the TrollStore app.  TrollHelper does not call this.
- (void)enableForTrollStore;

/// Whether this process has opted into the gate.
@property(nonatomic, readonly) BOOL enforcementEnabled;

/// Whether operations are currently allowed.
@property(nonatomic, readonly) BOOL operationAllowed;

/// Human-readable state shown in the visible lock screen/alert.
@property(nonatomic, readonly) NSString *statusMessage;

/// Run a status check.  Completion is always delivered on the main queue.
- (void)checkWithPresenter:(UIViewController *)presenter
                completion:(void (^)(BOOL allowed))completion;

/// Show a non-destructive frozen/offline message when an operation is attempted.
- (void)presentBlockedMessageFrom:(UIViewController *)presenter;

@end
