var HeaderAnimator = (function() {

	function HSLA(h, s, l, a) {
		this.h = h || 208;
		this.s = s || 56;
		this.l = l || 53;
		this.a = a || 1;
	}

	HSLA.prototype.toString = function() {
		return 'hsla(' + ([this.h, this.s+'%', this.l+'%', this.a].join(',')) + ')';
	};

	function Particle(digit, x, y, vx, vy, hsla) {
		this.digit = digit || '0';
		this.x = x;
		this.y = y;
		this.vx = vx;
		this.vy = vy;
		this.hsla = hsla || new HSLA();
	}

	function HeaderAnimator(canvas_id) {
		this.frame_count = 0;
		this.running = false;
		this.target_fps = 60;
		this.start_ts = 0;
		this.now = null;
		this.then = null;
		this.elapsed = 0;
		this.boundtick = null;
		this.canvas = document.getElementById(canvas_id);

		this.particles = [];
	}

	HeaderAnimator.prototype.start = function() {
		this.running = true;
		window.requestAnimationFrame(this.boundtick);
	};

	HeaderAnimator.prototype.stop = function() {
		this.running = false;
	};

	HeaderAnimator.prototype.init = function() {
		this.boundtick = this.tick.bind(this);

		this.canvas.width = window.innerWidth;
		//this.canvas.height = window.innerHeight;

		this.c = this.canvas.getContext('2d');
		this.clear();

		for (var i = 0; i < 50; i++) {
			this.particles.push(this.create_particle());
		}
	};

	HeaderAnimator.prototype.clear = function() {
		this.c.clearRect(0, 0, this.canvas.width, this.canvas.height);
	};

	HeaderAnimator.prototype.tick = function(ts) {
		if (!this.running) return;

		window.requestAnimationFrame(this.boundtick);

		this.now = ts;
		this.elapsed = this.now - this.then;

		if (this.elapsed > this.target_fps) {
			this.then = this.now - (this.elapsed % this.target_fps);
			this.clear();
			this.update(ts);
		}
	};

	HeaderAnimator.prototype.create_particle = function() {
		var digit = Math.random() > 0.5 ? '0' : '1',
			hsla = new HSLA(0, 0, 0, 0.1*Math.random()),
			p = new Particle(digit, this.canvas.width, (Math.floor(Math.random()*this.canvas.height/14)*14), -Math.random(), 0.0, hsla);

		return p;
	};

	HeaderAnimator.prototype.update = function(ts) {
		var p = null, remove = [], idx = 0, i;

		for (i = 0; i < this.particles.length; i++) {
			p = this.particles[i];

			p.vx -= 0.01; // ACCELERATE

			p.x += p.vx;
			p.y += p.vy;

			if (p.x < 0) {
				remove.push(p);
			}

			this.c.beginPath();

			this.c.font = '18pt Arial';

			this.c.fillStyle = p.hsla.toString();
			this.c.strokeStyle = p.hsla.toString();
			//this.c.fillText(p.digit, p.x, p.y);
			this.c.strokeText(p.digit, p.x, p.y);
		}

		for (i = remove.length - 1; i >= 0; i--) {
			idx = this.particles.indexOf(remove[i]);
			p = this.particles.splice(idx,1);
			delete p;
		};

		if (Math.random() * 10 > 7) {
			this.particles.push(this.create_particle());
		}
	};

	return HeaderAnimator;

}());