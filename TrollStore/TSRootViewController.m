#import "TSRootViewController.h"
#import "TSAppTableViewController.h"
#import "TSSettingsListController.h"
#import <TSPresentationDelegate.h>
#import "JumoLicenseGate.h"

@interface TSRootViewController ()
@property(nonatomic, strong) UIView *jumoLicenseOverlay;
@end

@implementation TSRootViewController

- (void)loadView
{
	[super loadView];

	TSAppTableViewController* appTableVC = [[TSAppTableViewController alloc] init];
	appTableVC.title = @"应用";

	TSSettingsListController* settingsListVC = [[TSSettingsListController alloc] init];
	settingsListVC.title = @"设置";

	UINavigationController* appNavigationController = [[UINavigationController alloc] initWithRootViewController:appTableVC];
	UINavigationController* settingsNavigationController = [[UINavigationController alloc] initWithRootViewController:settingsListVC];

	appNavigationController.tabBarItem.image = [UIImage systemImageNamed:@"square.stack.3d.up.fill"];
	settingsNavigationController.tabBarItem.image = [UIImage systemImageNamed:@"gear"];

	self.title = @"巨魔苹果玩家";
	self.viewControllers = @[appNavigationController, settingsNavigationController];
}

- (void)viewDidLoad
{
	[super viewDidLoad];

	TSPresentationDelegate.presentationViewController = self;
	[[JumoLicenseGate sharedGate] enableForTrollStore];
	[[NSNotificationCenter defaultCenter] addObserver:self
		selector:@selector(refreshJumoLicense)
		name:UIApplicationWillEnterForegroundNotification
		object:nil];
}

- (void)viewDidAppear:(BOOL)animated
{
	[super viewDidAppear:animated];
	[self refreshJumoLicense];
}

- (void)refreshJumoLicense
{
	JumoLicenseGate *gate = [JumoLicenseGate sharedGate];
	[gate checkWithPresenter:self completion:^(BOOL allowed) {
		if(allowed)
		{
			[self.jumoLicenseOverlay removeFromSuperview];
			self.jumoLicenseOverlay = nil;
		}
		else
		{
			[self showJumoLicenseOverlay];
		}
	}];
}

- (void)showJumoLicenseOverlay
{
	if(self.jumoLicenseOverlay) return;

	UIView *overlay = [[UIView alloc] initWithFrame:self.view.bounds];
	overlay.autoresizingMask = UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight;
	overlay.backgroundColor = [UIColor systemBackgroundColor];
	overlay.userInteractionEnabled = YES;

	UIImageView *icon = [[UIImageView alloc] initWithImage:[UIImage systemImageNamed:@"lock.shield.fill"]];
	icon.tintColor = [UIColor systemRedColor];
	icon.translatesAutoresizingMaskIntoConstraints = NO;
	[overlay addSubview:icon];

	UILabel *title = [UILabel new];
	title.text = @"\u5de8\u9b54\u5546\u5e97\u6682\u4e0d\u53ef\u7528";
	title.font = [UIFont systemFontOfSize:24 weight:UIFontWeightSemibold];
	title.textAlignment = NSTextAlignmentCenter;
	title.translatesAutoresizingMaskIntoConstraints = NO;
	[overlay addSubview:title];

	UILabel *message = [UILabel new];
	message.text = [JumoLicenseGate sharedGate].statusMessage ?: @"\u6388\u6743\u5df2\u51bb\u7ed3\uff0c\u8bf7\u8054\u7cfb\u5ba2\u670d";
	message.textColor = [UIColor secondaryLabelColor];
	message.numberOfLines = 0;
	message.textAlignment = NSTextAlignmentCenter;
	message.translatesAutoresizingMaskIntoConstraints = NO;
	[overlay addSubview:message];

	UIButton *retry = [UIButton buttonWithType:UIButtonTypeSystem];
	[retry setTitle:@"\u91cd\u65b0\u9a8c\u8bc1" forState:UIControlStateNormal];
	[retry addAction:[UIAction actionWithHandler:^(__kindof UIAction *action) {
		[self.jumoLicenseOverlay removeFromSuperview];
		self.jumoLicenseOverlay = nil;
		[self refreshJumoLicense];
	}] forControlEvents:UIControlEventTouchUpInside];
	retry.translatesAutoresizingMaskIntoConstraints = NO;
	[overlay addSubview:retry];

	[self.view addSubview:overlay];
	self.jumoLicenseOverlay = overlay;
	[NSLayoutConstraint activateConstraints:@[
		[icon.centerXAnchor constraintEqualToAnchor:overlay.centerXAnchor],
		[icon.topAnchor constraintEqualToAnchor:overlay.safeAreaLayoutGuide.topAnchor constant:120],
		[icon.widthAnchor constraintEqualToConstant:52],
		[icon.heightAnchor constraintEqualToConstant:52],
		[title.topAnchor constraintEqualToAnchor:icon.bottomAnchor constant:18],
		[title.leadingAnchor constraintEqualToAnchor:overlay.leadingAnchor constant:24],
		[title.trailingAnchor constraintEqualToAnchor:overlay.trailingAnchor constant:-24],
		[message.topAnchor constraintEqualToAnchor:title.bottomAnchor constant:12],
		[message.leadingAnchor constraintEqualToAnchor:overlay.leadingAnchor constant:32],
		[message.trailingAnchor constraintEqualToAnchor:overlay.trailingAnchor constant:-32],
		[retry.topAnchor constraintEqualToAnchor:message.bottomAnchor constant:24],
		[retry.centerXAnchor constraintEqualToAnchor:overlay.centerXAnchor]
	]];
}

@end
