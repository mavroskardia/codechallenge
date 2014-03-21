
(function () {

	$(document).ready(function () {
		var header_animator = new HeaderAnimator('binary_canvas');
		header_animator.init();
		header_animator.start();

		var nav_handler = new NavHandler('main_nav');
		nav_handler.init();
	});

}());