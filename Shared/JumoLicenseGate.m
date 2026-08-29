#import "JumoLicenseGate.h"

#import <dlfcn.h>

static NSString * const JumoLicenseEndpoint = @"http://124.223.199.167/api/trollstore_license.php";
static NSTimeInterval const JumoOfflineGracePeriod = 72.0 * 60.0 * 60.0;

@interface JumoLicenseGate ()
@property(nonatomic, readwrite) BOOL enforcementEnabled;
@property(nonatomic, readwrite) BOOL operationAllowed;
@property(nonatomic, readwrite, copy) NSString *statusMessage;
@property(nonatomic, copy) NSString *deviceIdentifier;
@property(nonatomic) BOOL checking;
@property(nonatomic) BOOL presentingCodePrompt;
@end

@implementation JumoLicenseGate

+ (instancetype)sharedGate
{
	static JumoLicenseGate *gate;
	static dispatch_once_t onceToken;
	dispatch_once(&onceToken, ^{
		gate = [JumoLicenseGate new];
	});
	return gate;
}

- (instancetype)init
{
	self = [super init];
	if(self)
	{
		_statusMessage = @"\u6b63\u5728\u9a8c\u8bc1\u6388\u6743\u72b6\u6001\u2026";
		_deviceIdentifier = [self.class currentDeviceIdentifier];
		[self restoreCachedState];
	}
	return self;
}

+ (NSString *)currentDeviceIdentifier
{
	// The PC installer has the lockdown UDID.  On the device, try the same
	// MobileGestalt value first so the existing one-code/one-device binding can
	// be checked without asking the employee to reconnect a computer.
	void *handle = dlopen("/usr/lib/libMobileGestalt.dylib", RTLD_LAZY);
	if(handle)
	{
		typedef CFTypeRef (*MGCopyAnswerFunction)(CFStringRef);
		MGCopyAnswerFunction copyAnswer = (MGCopyAnswerFunction)dlsym(handle, "MGCopyAnswer");
		if(copyAnswer)
		{
			CFTypeRef value = copyAnswer(CFSTR("UniqueDeviceID"));
			if(value && CFGetTypeID(value) == CFStringGetTypeID())
			{
				NSString *identifier = [(__bridge NSString *)value copy];
				CFRelease(value);
				dlclose(handle);
				if(identifier.length) return identifier.uppercaseString;
			}
			else if(value)
			{
				CFRelease(value);
			}
		}
		dlclose(handle);
	}

	NSString *vendorIdentifier = UIDevice.currentDevice.identifierForVendor.UUIDString;
	if(vendorIdentifier.length) return vendorIdentifier.uppercaseString;

	// Last-resort stable identifier for environments where MobileGestalt and
	// identifierForVendor are unavailable.  This is only a fallback for test
	// builds and is kept in the app's preferences.
	NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
	NSString *fallback = [defaults stringForKey:@"jumo.device_identifier"];
	if(!fallback.length)
	{
		fallback = [NSUUID UUID].UUIDString;
		[defaults setObject:fallback forKey:@"jumo.device_identifier"];
		[defaults synchronize];
	}
	return fallback.uppercaseString;
}

- (void)restoreCachedState
{
	NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
	NSString *code = [defaults stringForKey:@"jumo.license_code"];
	NSDate *lastSuccess = [defaults objectForKey:@"jumo.license_last_success"];
	if(code.length && [lastSuccess isKindOfClass:NSDate.class] &&
	   [[NSDate date] timeIntervalSinceDate:lastSuccess] <= JumoOfflineGracePeriod)
	{
		_operationAllowed = YES;
		_statusMessage = @"\u6388\u6743\u6709\u6548\uff08\u79bb\u7ebf\u5bbd\u9650\u671f\uff09";
	}
}

- (void)enableForTrollStore
{
	self.enforcementEnabled = YES;
	if(!self.operationAllowed)
	{
		self.statusMessage = @"\u6b63\u5728\u9a8c\u8bc1\u6388\u6743\u72b6\u6001\u2026";
	}
}

- (NSString *)formEncode:(NSString *)value
{
	NSCharacterSet *allowed = [NSCharacterSet characterSetWithCharactersInString:@"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~"];
	return [value ?: @"" stringByAddingPercentEncodingWithAllowedCharacters:allowed] ?: @"";
}

- (void)complete:(void (^)(BOOL))completion allowed:(BOOL)allowed
{
	dispatch_async(dispatch_get_main_queue(), ^{
		if(completion) completion(allowed);
	});
}

- (void)promptForCodeFrom:(UIViewController *)presenter completion:(void (^)(BOOL))completion
{
	if(!presenter)
	{
		[self complete:completion allowed:NO];
		return;
	}
	if(self.presentingCodePrompt)
	{
		[self complete:completion allowed:self.operationAllowed];
		return;
	}
	self.presentingCodePrompt = YES;

	UIAlertController *alert = [UIAlertController alertControllerWithTitle:@"\u8f93\u5165\u6fc0\u6d3b\u7801"
		message:@"\u8bf7\u8f93\u5165\u5df2\u7ed1\u5b9a\u6b64\u8bbe\u5907\u7684\u6fc0\u6d3b\u7801\u3002\u6fc0\u6d3b\u7801\u53ea\u7ed1\u5b9a\u4e00\u53f0\u8bbe\u5907\u3002"
		preferredStyle:UIAlertControllerStyleAlert];
	[alert addTextFieldWithConfigurationHandler:^(UITextField *field) {
		field.placeholder = @"\u6fc0\u6d3b\u7801";
		field.autocapitalizationType = UITextAutocapitalizationTypeAllCharacters;
		field.clearButtonMode = UITextFieldViewModeWhileEditing;
	}];
	__weak typeof(self) weakSelf = self;
	UIAlertAction *cancel = [UIAlertAction actionWithTitle:@"\u53d6\u6d88" style:UIAlertActionStyleCancel handler:^(UIAlertAction *action) {
		weakSelf.presentingCodePrompt = NO;
		[weakSelf complete:completion allowed:weakSelf.operationAllowed];
	}];
	UIAlertAction *verify = [UIAlertAction actionWithTitle:@"\u9a8c\u8bc1" style:UIAlertActionStyleDefault handler:^(UIAlertAction *action) {
		JumoLicenseGate *strongSelf = weakSelf;
		strongSelf.presentingCodePrompt = NO;
		NSString *code = [alert.textFields.firstObject.text stringByTrimmingCharactersInSet:NSCharacterSet.whitespaceAndNewlineCharacterSet];
		if(!code.length)
		{
			strongSelf.statusMessage = @"\u672a\u8f93\u5165\u6fc0\u6d3b\u7801";
			[strongSelf complete:completion allowed:NO];
			return;
		}
		[[NSUserDefaults standardUserDefaults] setObject:code forKey:@"jumo.license_code"];
		[strongSelf checkWithPresenter:nil completion:completion];
	}];
	[alert addAction:cancel];
	[alert addAction:verify];
	[presenter presentViewController:alert animated:YES completion:nil];
}

- (void)checkWithPresenter:(UIViewController *)presenter completion:(void (^)(BOOL))completion
{
	if(!self.enforcementEnabled)
	{
		[self complete:completion allowed:YES];
		return;
	}
	NSString *code = [[NSUserDefaults standardUserDefaults] stringForKey:@"jumo.license_code"];
	if(!code.length)
	{
		[self promptForCodeFrom:presenter completion:completion];
		return;
	}
	if(self.checking)
	{
		[self complete:completion allowed:self.operationAllowed];
		return;
	}
	self.checking = YES;
	self.statusMessage = @"\u6b63\u5728\u9a8c\u8bc1\u6388\u6743\u72b6\u6001\u2026";

	NSString *bodyString = [NSString stringWithFormat:@"code=%@&udid=%@&ts=%lld",
		[self formEncode:code], [self formEncode:self.deviceIdentifier], (long long)[[NSDate date] timeIntervalSince1970]];
	NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:JumoLicenseEndpoint]
		cachePolicy:NSURLRequestReloadIgnoringLocalCacheData timeoutInterval:15.0];
	request.HTTPMethod = @"POST";
	request.HTTPBody = [bodyString dataUsingEncoding:NSUTF8StringEncoding];
	[request setValue:@"application/x-www-form-urlencoded; charset=utf-8" forHTTPHeaderField:@"Content-Type"];

	__weak typeof(self) weakSelf = self;
	NSURLSessionDataTask *task = [NSURLSession.sharedSession dataTaskWithRequest:request completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
		JumoLicenseGate *strongSelf = weakSelf;
		if(!strongSelf) return;
		strongSelf.checking = NO;
		BOOL allowed = NO;
		NSString *message = @"\u6388\u6743\u9a8c\u8bc1\u5931\u8d25\uff0c\u8bf7\u8054\u7cfb\u5ba2\u670d";
		if(!error && data.length)
		{
			NSError *jsonError = nil;
			NSDictionary *json = [NSJSONSerialization JSONObjectWithData:data options:0 error:&jsonError];
			NSString *status = [json[@"status"] isKindOfClass:NSString.class] ? [json[@"status"] lowercaseString] : @"";
			NSString *serverMessage = [json[@"msg"] isKindOfClass:NSString.class] ? json[@"msg"] : @"";
			BOOL statusOK = !status.length || [status isEqualToString:@"active"] || [status isEqualToString:@"ok"];
			if([json[@"ok"] boolValue] && statusOK)
			{
				allowed = YES;
				message = @"\u6388\u6743\u6709\u6548";
				[[NSUserDefaults standardUserDefaults] setObject:[NSDate date] forKey:@"jumo.license_last_success"];
				[[NSUserDefaults standardUserDefaults] synchronize];
			}
			else if([status isEqualToString:@"frozen"] || [status isEqualToString:@"expired"] ||
					[serverMessage rangeOfString:@"frozen" options:NSCaseInsensitiveSearch].location != NSNotFound ||
					[serverMessage rangeOfString:@"expired" options:NSCaseInsensitiveSearch].location != NSNotFound)
			{
				allowed = NO;
				message = [status isEqualToString:@"expired"] ? @"\u6388\u6743\u5df2\u5230\u671f\uff0c\u8bf7\u8054\u7cfb\u5ba2\u670d" : @"\u6388\u6743\u5df2\u51bb\u7ed3\uff0c\u8bf7\u8054\u7cfb\u5ba2\u670d";
			}
			else
			{
				allowed = NO;
				message = serverMessage.length ? serverMessage : @"\u6fc0\u6d3b\u7801\u672a\u7ed1\u5b9a\u6b64\u8bbe\u5907";
			}
		}
		else
		{
			NSDate *lastSuccess = [[NSUserDefaults standardUserDefaults] objectForKey:@"jumo.license_last_success"];
			if([lastSuccess isKindOfClass:NSDate.class] && [[NSDate date] timeIntervalSinceDate:lastSuccess] <= JumoOfflineGracePeriod)
			{
				allowed = YES;
				message = @"\u6388\u6743\u670d\u52a1\u5668\u6682\u65f6\u4e0d\u53ef\u7528\uff0c\u5904\u4e8e\u79bb\u7ebf\u5bbd\u9650\u671f";
			}
			else
			{
				allowed = NO;
				message = @"\u65e0\u6cd5\u8fde\u63a5\u6388\u6743\u670d\u52a1\u5668\uff0c\u8bf7\u68c0\u67e5\u7f51\u7edc\u540e\u91cd\u8bd5";
			}
		}
		strongSelf.operationAllowed = allowed;
		strongSelf.statusMessage = message;
		[strongSelf complete:completion allowed:allowed];
	}];
	[task resume];
}

- (void)presentBlockedMessageFrom:(UIViewController *)presenter
{
	if(!self.enforcementEnabled || self.operationAllowed || !presenter) return;
	NSString *message = self.statusMessage.length ? self.statusMessage : @"\u6388\u6743\u5df2\u51bb\u7ed3\uff0c\u8bf7\u8054\u7cfb\u5ba2\u670d";
	UIAlertController *alert = [UIAlertController alertControllerWithTitle:@"\u5de8\u9b54\u5546\u5e97\u6682\u4e0d\u53ef\u7528"
		message:message preferredStyle:UIAlertControllerStyleAlert];
	[alert addAction:[UIAlertAction actionWithTitle:@"\u5173\u95ed" style:UIAlertActionStyleDefault handler:nil]];
	[presenter presentViewController:alert animated:YES completion:nil];
}

@end
