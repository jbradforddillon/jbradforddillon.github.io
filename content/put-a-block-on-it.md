Title: Put a Block on It
Slug: put-a-block-on-it
Date: 2013-06-04 21:04:35
Tags: objc, api
Category: objective-c
Author: 
Lang: 

_This article was originally posted on the [Double Encore Insights blog](http://www.doubleencore.com/2013/04/put-a-block-on-it/) on April 30th, 2013_

Collin Donnell, proprietor of Portland-based Albina Development, recently [wrote an article](http://collindonnell.com/2013/04/07/stop-using-success-failure-blocks/) urging developers to stop the somewhat common practice of using separate blocks for success and failure cases in asynchronous operations. Instead, Collin suggests writing methods that accept a single completion block designed to handle either case. To summarize his point of view, using separate success and failure blocks will likely lead to duplicate code, and it’s not “the Apple way”.

A great example of this single completion block pattern from Apple’s own APIs is found in one of NSURLConnection’s newer async methods. The sendAsynchronousRequest method was added in iOS 5.0, and provides a single completionHandler argument to handle any result.

	:::objc
	+ (void)sendAsynchronousRequest:(NSURLRequest *)request 
							  queue:(NSOperationQueue *)queue 
				  completionHandler:(void (^)(NSURLResponse *, NSData *, NSError *))handler;

Collin’s article sparked the urge to do some refactoring. We have several internal libraries with async methods that are currently designed to have two, and in some cases even three, separate callback blocks. These libraries have been in use for a long time, and were originally designed to use delegation. With the delegation pattern, there is typically a one-to-one relationship between signal and outcome. For an example, we need look no further than NSURLConnection’s own delegate methods:

	:::objc
	- (void)connectionDidFinishLoading:(NSURLConnection *)connection;
	- (void)connection:(NSURLConnection *)connection didFailWithError:(NSError *)error;

When converting a library that uses delegation to blocks, or perhaps more importantly when adding blocks as an option to such a library, the path of least resistance is generally to add a block for every delegate method. This thinking leads to the pattern that Collin is arguing against.

	:::objc
	// Classic delegation
	- (void)myOperationDidSucceed:(id data) {
		[myView hideLoadingIndicator];
		// Do something with data
	}
	
	- (void)myOperationDidFail:(NSError *)error {
		[myView hideLoadingIndicator];
		// Do something with the error
	}
	
	- (void)myOperationDidReachAnotherOutcome:(NSDictionary *info) {
		[myView hideLoadingIndicator];
		// Do something with info
	}
	
	// Separate blocks
	[myOperation startOperatingWithSuccess:^(id data) {
		[myView hideLoadingIndicator];
		// Do something with data
	
	} failure:^(NSError *error) {
		[myView hideLoadingIndicator];
		// Do something with the error
	
	} anotherPossibleOutcome:^(NSDictionary *info) {
		[myView hideLoadingIndicator];
		// Do something with info
	}];

So what’s the harm? Having one signal per outcome has served us well for years. Why do we need to change now?

Stylistically, we’re talking about where to put the curly braces. Do you want to use them to encapsulate separate blocks, or do you want to use them for flow control within a single block? If this were the only concern, it would definitely be more of a personal preference issue. Inlining several blocks within an async task’s initialization method can get ugly (do you line up with the parameter colons, or with the indentation level?). On the other hand, so can several levels of conditionals. But beyond code formatting, in terms of nuts and bolts, we’re talking about efficiency, on several different levels.

## Efficiency Begets Efficiency

As Collin notes, there are often common tasks that occur in both success and failure blocks. A good example would be hiding some loading UI or turning off the app’s activity indicator. This can result in duplicate code, or at least unnecessary abstractions. Having a single block means you only have to write that code once.

Having one block also means you have to do some value checking to determine what the final state of the async task was, and how to respond. Since you’re combining multiple outcomes into one signal, you need to determine the state before you act on it. One could argue that this results in unnecessary boilerplate code, but that’s only looking at one side of the API. In the multiple block pattern, the async task itself would likely use the same or similar logic to determine which block to execute. Moving that logic client-side can allow the task’s code to be written more efficiently, and can put the decision of “what to do next” more firmly in the client’s hands.

Let’s go back to that sendAsynchronousRequest method and look more closely at the completion handler:

	:::objc
	+ (void)sendAsynchronousRequest:(NSURLRequest *)request 
							  queue:(NSOperationQueue *)queue 
				  completionHandler:(void (^)(NSURLResponse *, NSData *, NSError *))handler;

Notice that the block is equipped to handle any result, and more importantly, almost any basic developer need. You get more than just data and an error. You get data, an error, and a complete NSURLResponse, which encapsulates significantly more information about the completed task. This allows your code to be much more nimble within that block. You have more than enough information to handle any completion outcome in a single signal. Go nuts.

	:::objc
	// One completion handler
	[myOperation startOperatingWithCompletionHandler:^(id data, NSError *error, NSDictionary *info) {
		[myView hideLoadingIndicator];
		if (error) {
			// Do something with the error
		}
	
		// Do something with data and/or info
	}];

## Efficiency at a Lower Level

Blocks are objects. Blocks are allocated, messaged, copied, and retained in memory. All of those things take time and space. Async tasks (generally) only have a single outcome. It really shouldn’t be possible for a task to both succeed and fail at the same time (though sadly, sometimes it is). In general, that means only one completion block is going to be used, which means that any other completion blocks that were allocated and passed along are essentially just taking up space. This is a cost that the delegation design pattern doesn’t incur, so it’s easy to overlook when migrating to blocks.

Admittedly, blocks are tiny, and the likelihood of these unnecessary allocations causing problems is pretty much nil. Generally, the time and memory costs of allocating a block are not statistically significant, and shouldn’t be worried about. But fewer blocks also means fewer chances for “typos” that end up creating retain cycles, leaking memory, or messaging a garbage pointer. If you’re interested in making the tightest loop possible, the realization that these costs exist might help you remember to steer clear of unnecessary block allocation. Future you will thank present you.

## Living in a Block World

From a fundamental level, using blocks for async completion handling is completely different from delegation, and it should be handled differently. Blocks are handy, and they allow us to be more concise and efficient with our code. But if we treat them like encapsulated delegation methods, we’re not taking advantage of those benefits.

My thanks to [Collin](https://twitter.com/collindonnell) for writing the article that sparked our introspection. We’re refactoring our libraries and our code to be better block world citizens, and encourage everyone to adopt this pattern as well, whether for an open source library or private app-specific code.

