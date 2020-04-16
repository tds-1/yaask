CKEDITOR.editorConfig = function( config ) {
  // Define changes to default configuration here. For example:
  // config.language = 'fr';
  // config.uiColor = '#AADC6E';
  config.mathJaxLib = "//cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS-MML_HTMLorMML";
  config.latexServer = "https://elpiscart.com/cgi-bin/mathtex.cgi?";
  //'imgur'
  config.extraPlugins = 'mathjax,imgur,MathType';
  config.imgurClientId = 'afd7949d38a220b';

  config.toolbar = [
         ['Bold', 'Italic', 'Underline', 'HorizontalRule', 'Strike', 'Subscript', 'Superscript', 'RemoveFormat'],
         ['NumberedList', 'BulletedList', 'Blockquote'],
         ['Image', 'Table', 'Math'],
         ['Maximize'],
         ['Scayt', 'MathType', 'ChemType' ,'Mathjax', 'Imgur'],
         ['Source', 'Replace'],
         [ 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock' ]
     ];

  config.allowedContent = true;
  config.removeDialogTabs = 'image:Link;image:advanced';
  config.disableNativeSpellChecker = false;

};
