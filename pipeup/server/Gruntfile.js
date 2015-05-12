
module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    bowercopy: {
      options: {
        destPrefix: 'static/vendor'
      },
      libs: {
        files: {
          'js/jquery.js': 'jquery/dist/jquery.js',
          'js/reconnecting-websocket.js': 'reconnectingWebsocket/reconnecting-websocket.js',
          'css': 'skeleton/css',
          'css/fontawesome.css': 'font-awesome/css/font-awesome.css',
          'fonts': 'font-awesome/fonts'
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-bowercopy');

  grunt.registerTask('default', ['bowercopy']);
};
