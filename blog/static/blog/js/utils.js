NexT.utils = NexT.$u = {
    wrapImageWithFancyBox: function () {
        $('.content img').not('[hidden]').not('.group-picture img, .post-gallery img').each(function () {
            var $image = $(this);
            var imageTitle = $image.attr('title');
            var $imageWrapLink = $image.parent('a');
            if ($imageWrapLink.size() < 1) {
                var imageLink = ($image.attr('data-original')) ? this.getAttribute('data-original') : this.getAttribute('src');
                $imageWrapLink = $image.wrap('<a href="' + imageLink + '"></a>').parent('a');
            }
            $imageWrapLink.addClass('fancybox fancybox.image');
            $imageWrapLink.attr('rel', 'group');
            if (imageTitle) {
                $imageWrapLink.append('<p class="image-caption">' + imageTitle + '</p>');
                $imageWrapLink.attr('title', imageTitle);
            }
        });
        $('.fancybox').fancybox({helpers: {overlay: {locked: false}}});
    }, lazyLoadPostsImages: function () {
        $('#posts').find('img').lazyload({effect: 'fadeIn', threshold: 0});
    }, registerTabsTag: function () {
        var tNav = '.tabs ul.nav-tabs ';
        $(function () {
            $(window).bind('hashchange', function () {
                var tHash = location.hash;
                if (tHash !== '') {
                    $(tNav + 'li:has(a[href="' + tHash + '"])').addClass('active').siblings().removeClass('active');
                    $(tHash).addClass('active').siblings().removeClass('active');
                }
            }).trigger('hashchange');
        });
        $(tNav + '.tab').on('click', function (href) {
            href.preventDefault();
            if (!$(this).hasClass('active')) {
                $(this).addClass('active').siblings().removeClass('active');
                var tActive = $(this).find('a').attr('href');
                $(tActive).addClass('active').siblings().removeClass('active');
                if (location.hash !== '') {
                    history.pushState('', document.title, window.location.pathname + window.location.search);
                }
            }
        });
    }, registerESCKeyEvent: function () {
        $(document).on('keyup', function (event) {
            var shouldDismissSearchPopup = event.which === 27 && $('.search-popup').is(':visible');
            if (shouldDismissSearchPopup) {
                $('.search-popup').hide();
                $('.search-popup-overlay').remove();
                $('body').css('overflow', '');
            }
        });
    }, registerBackToTop: function () {
        var THRESHOLD = 50;
        var $top = $('.back-to-top');
        $(window).on('scroll', function () {
            $top.toggleClass('back-to-top-on', window.pageYOffset > THRESHOLD);
            var scrollTop = $(window).scrollTop();
            var contentVisibilityHeight = NexT.utils.getContentVisibilityHeight();
            var scrollPercent = (scrollTop) / (contentVisibilityHeight);
            var scrollPercentRounded = Math.round(scrollPercent * 100);
            var scrollPercentMaxed = (scrollPercentRounded > 100) ? 100 : scrollPercentRounded;
            $('#scrollpercent>span').html(scrollPercentMaxed);
        });
        $top.on('click', function () {
            $('body').velocity('scroll');
        });
    }, embeddedVideoTransformer: function () {
        var $iframes = $('iframe');
        var SUPPORTED_PLAYERS = ['www.youtube.com', 'player.vimeo.com', 'player.youku.com', 'music.163.com', 'www.tudou.com'];
        var pattern = new RegExp(SUPPORTED_PLAYERS.join('|'));
        $iframes.each(function () {
            var iframe = this;
            var $iframe = $(this);
            var oldDimension = getDimension($iframe);
            var newDimension;
            if (this.src.search(pattern) > 0) {
                var videoRatio = getAspectRadio(oldDimension.width, oldDimension.height);
                $iframe.width('100%').height('100%').css({
                    position: 'absolute',
                    top: '0',
                    left: '0'
                });
                var wrap = document.createElement('div');
                wrap.className = 'fluid-vids';
                wrap.style.position = 'relative';
                wrap.style.marginBottom = '20px';
                wrap.style.width = '100%';
                wrap.style.paddingTop = videoRatio + '%';
                (wrap.style.paddingTop === '') && (wrap.style.paddingTop = '50%');
                var iframeParent = iframe.parentNode;
                iframeParent.insertBefore(wrap, iframe);
                wrap.appendChild(iframe);
                if (this.src.search('music.163.com') > 0) {
                    newDimension = getDimension($iframe);
                    var shouldRecalculateAspect = newDimension.width > oldDimension.width || newDimension.height < oldDimension.height;
                    if (shouldRecalculateAspect) {
                        wrap.style.paddingTop = getAspectRadio(newDimension.width, oldDimension.height) + '%';
                    }
                }
            }
        });

        function getDimension($element) {
            return {width: $element.width(), height: $element.height()};
        }

        function getAspectRadio(width, height) {
            return height / width * 100;
        }
    }, addActiveClassToMenuItem: function () {
        var path = window.location.pathname;
        path = path === '/' ? path : path.substring(0, path.length - 1);
        $('.menu-item a[href^="' + path + '"]:first').parent().addClass('menu-item-active');
    }, hasMobileUA: function () {
        var nav = window.navigator;
        var ua = nav.userAgent;
        var pa = /iPad|iPhone|Android|Opera Mini|BlackBerry|webOS|UCWEB|Blazer|PSP|IEMobile|Symbian/g;
        return pa.test(ua);
    }, isTablet: function () {
        return window.screen.width < 992 && window.screen.width > 767 && this.hasMobileUA();
    }, isMobile: function () {
        return window.screen.width < 767 && this.hasMobileUA();
    }, isDesktop: function () {
        return !this.isTablet() && !this.isMobile();
    }, escapeSelector: function (selector) {
        return selector.replace(/[!"$%&'()*+,.\/:;<=>?@[\\\]^`{|}~]/g, '\\$&');
    }, displaySidebar: function () {
        if (!this.isDesktop() || this.isPisces() || this.isGemini()) {
            return;
        }
        $('.sidebar-toggle').trigger('click');
    }, isMist: function () {
        return CONFIG.scheme === 'Mist';
    }, isPisces: function () {
        return CONFIG.scheme === 'Pisces';
    }, isGemini: function () {
        return CONFIG.scheme === 'Gemini';
    }, getScrollbarWidth: function () {
        var $div = $('<div />').addClass('scrollbar-measure').prependTo('body');
        var div = $div[0];
        var scrollbarWidth = div.offsetWidth - div.clientWidth;
        $div.remove();
        return scrollbarWidth;
    }, getContentVisibilityHeight: function () {
        var docHeight = $('#content').height(), winHeight = $(window).height(),
            contentVisibilityHeight = (docHeight > winHeight) ? (docHeight - winHeight) : ($(document).height() - winHeight);
        return contentVisibilityHeight;
    }, getSidebarb2tHeight: function () {
        var sidebarb2tHeight = (CONFIG.sidebar.b2t) ? $('.back-to-top').height() : 0;
        return sidebarb2tHeight;
    }, getSidebarSchemePadding: function () {
        var sidebarNavHeight = ($('.sidebar-nav').css('display') == 'block') ? $('.sidebar-nav').outerHeight(true) : 0,
            sidebarInner = $('.sidebar-inner'),
            sidebarPadding = sidebarInner.innerWidth() - sidebarInner.width(),
            sidebarSchemePadding = this.isPisces() || this.isGemini() ? ((sidebarPadding * 2) + sidebarNavHeight + (CONFIG.sidebar.offset * 2) + this.getSidebarb2tHeight()) : ((sidebarPadding * 2) + (sidebarNavHeight / 2));
        return sidebarSchemePadding;
    }
};
$(document).ready(function () {
    initSidebarDimension();

    function initSidebarDimension() {
        var updateSidebarHeightTimer;
        $(window).on('resize', function () {
            updateSidebarHeightTimer && clearTimeout(updateSidebarHeightTimer);
            updateSidebarHeightTimer = setTimeout(function () {
                var sidebarWrapperHeight = document.body.clientHeight - NexT.utils.getSidebarSchemePadding();
                updateSidebarHeight(sidebarWrapperHeight);
            }, 0);
        });
        var scrollbarWidth = NexT.utils.getScrollbarWidth();
        if ($('.site-overview-wrap').height() > (document.body.clientHeight - NexT.utils.getSidebarSchemePadding())) {
            $('.site-overview').css('width', 'calc(100% + ' + scrollbarWidth + 'px)');
        }
        if ($('.post-toc-wrap').height() > (document.body.clientHeight - NexT.utils.getSidebarSchemePadding())) {
            $('.post-toc').css('width', 'calc(100% + ' + scrollbarWidth + 'px)');
        }
        updateSidebarHeight(document.body.clientHeight - NexT.utils.getSidebarSchemePadding());
    }

    function updateSidebarHeight(height) {
        height = height || 'auto';
        $('.site-overview, .post-toc').css('max-height', height);
    }
});