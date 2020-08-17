var gulp = require('gulp');
var cssnano = require('gulp-cssnano');
var rename = require('gulp-rename');
var uglify = require('gulp-uglify');
var concat = require('gulp-concat');
var imagemin = require('gulp-imagemin');
var cache = require('gulp-cache');
var bs = require('browser-sync').create();
var sass = require('gulp-sass');

var util = require('gulp-util');
var sourcemaps = require('gulp-sourcemaps');

var path = {
    'html': './templates/**/',
    'css': './src/css/',
    'js': './src/js/',
    'images': './src/images/',
    'css_dist': './dist/css/',
    'js_dist': './dist/js/',
    'images_dist': './dist/images/'
};

gulp.task('html', function () {
    gulp.src(path.html + '*.html')
        .pipe(bs.stream())
});


gulp.task('css', function () {
	gulp.src(path.css + '*.scss')
        .pipe(sass().on('error',sass.logError))   //如果sass语法出现错误只会将错误打印出来，不会终止任务
	    .pipe(cssnano())
	    .pipe(rename({'suffix':'.min'}))
	    .pipe(gulp.dest(path.css_dist))
	    .pipe(bs.stream())
});


gulp.task('js', function () {
	gulp.src(path.js + '*.js')
		.pipe(sourcemaps.init())
	    //.pipe(concat('index.js'))
	    .pipe(uglify().on('error', util.log))
	    .pipe(rename({'suffix':'.min'}))
		.pipe(sourcemaps.write())
	    .pipe(gulp.dest(path.js_dist))
	    .pipe(bs.stream())
});


gulp.task('images', function () {
	gulp.src(path.images + '*.*')
	    .pipe(cache(imagemin()))
	    .pipe(gulp.dest(path.images_dist))
	    .pipe(bs.stream())
});


gulp.task('watch', function () {
    gulp.watch(path.html + '*.html', ['html']);
	gulp.watch(path.css + '*.scss', ['css']);
	gulp.watch(path.js + '*.js', ['js']);
	gulp.watch(path.images + '*.*', ['images'])
});


gulp.task('bs', function () {
	bs.init({
		'server':{
			'baseDir': './'
		}
	});
});


//gulp.task('default', ['bs', 'watch']);
gulp.task('default', ['watch']);