/*
 * Stopwatch — counts the seconds spent on one question.
 * It only runs while the page is visible and the stopwatch is not paused (a flagged question is paused).
 */
(function (root) {
  'use strict';

  function Stopwatch(startSeconds, onTick) {
    this.base = startSeconds || 0;   // seconds accumulated before the current run
    this.since = null;               // timestamp of the current run, or null when stopped
    this.paused = false;
    this.onTick = onTick || null;
    this._iv = null;
    var self = this;
    this._vis = function () {
      if (document.hidden) self._stopRun();
      else if (!self.paused && self._wanted) self._startRun();
    };
    document.addEventListener('visibilitychange', this._vis);
  }

  Stopwatch.prototype._startRun = function () {
    if (this.since !== null) return;
    this.since = Date.now();
    var self = this;
    this._iv = setInterval(function () { if (self.onTick) self.onTick(self.elapsed()); }, 1000);
  };
  Stopwatch.prototype._stopRun = function () {
    if (this.since === null) return;
    this.base += (Date.now() - this.since) / 1000;
    this.since = null;
    clearInterval(this._iv);
  };
  Stopwatch.prototype.start = function () {
    this._wanted = true;
    if (!this.paused && !document.hidden) this._startRun();
    if (this.onTick) this.onTick(this.elapsed());
    return this;
  };
  Stopwatch.prototype.pause = function () { this.paused = true; this._stopRun(); if (this.onTick) this.onTick(this.elapsed()); };
  Stopwatch.prototype.resume = function () { this.paused = false; if (this._wanted && !document.hidden) this._startRun(); if (this.onTick) this.onTick(this.elapsed()); };
  Stopwatch.prototype.stop = function () { this._wanted = false; this._stopRun(); return this.elapsed(); };
  Stopwatch.prototype.reset = function (sec) { this._stopRun(); this.base = sec || 0; if (this._wanted && !this.paused) this._startRun(); };
  Stopwatch.prototype.elapsed = function () {
    return this.base + (this.since !== null ? (Date.now() - this.since) / 1000 : 0);
  };
  Stopwatch.prototype.destroy = function () {
    this.stop();
    document.removeEventListener('visibilitychange', this._vis);
  };

  root.Stopwatch = Stopwatch;
})(window);
