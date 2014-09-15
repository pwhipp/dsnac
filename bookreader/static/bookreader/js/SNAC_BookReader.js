function SNAC_BookReader(){
    BookReader.apply(this);
}

SNAC_BookReader.prototype.__proto__ = BookReader.prototype;

(function ($) {
SNAC_BookReader.prototype.initUIStrings = function()
{
    // Navigation handlers will be bound after all UI is in place -- makes moving icons between
    // the toolbar and nav bar easier

    // Setup tooltips -- later we could load these from a file for i18n
    var titles = { '.logo': 'Return to home page', // $$$ update after getting OL record
                   '.zoom_in': 'Zoom in',
                   '.zoom_out': 'Zoom out',
                   '.onepg': 'One-page view',
                   '.twopg': 'Two-page view',
                   '.thumb': 'Thumbnail view',
                   '.print': 'Print this page',
                   '.embed': 'Embed BookReader',
                   '.link': 'Link to this book (and page)',
                   '.bookmark': 'Bookmark this page',
                   '.read': 'Read this book aloud',
                   '.share': 'Share this book',
                   '.info': 'About this book',
                   '.full': 'Show fullscreen',
                   '.book_left': 'Flip left',
                   '.book_right': 'Flip right',
                   '.book_up': 'Page up',
                   '.book_down': 'Page down',
                   '.play': 'Play',
                   '.pause': 'Pause',
                   '.BRdn': 'Show/hide nav bar', // Would have to keep updating on state change to have just "Hide nav bar"
                   '.BRup': 'Show/hide nav bar',
                   '.book_top': 'First page',
                   '.book_bottom': 'Last page'
                  };
    if ('rl' == this.pageProgression) {
        titles['.book_leftmost'] = 'Last page';
        titles['.book_rightmost'] = 'First page';
    } else { // LTR
        titles['.book_leftmost'] = 'First page';
        titles['.book_rightmost'] = 'Last page';
    }

    for (var icon in titles) {
        if (titles.hasOwnProperty(icon)) {
            $('#BookReader').find(icon).attr('title', titles[icon]);
        }
    }
}
})(jQuery);