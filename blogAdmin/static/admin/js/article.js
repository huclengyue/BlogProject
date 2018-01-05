var mditor, htmlEditor;
var tale = new $.tale();
var attach_url = $('#attach_url').val();
// 每60秒自动保存一次草稿
var refreshIntervalId = setInterval("autoSave()", 60 * 1000);
var token = document.getElementById('article').getAttribute('data');
$(document).ready(function () {

    mditor = window.mditor = Mditor.fromTextarea(document.getElementById('md-editor'));
    // 富文本编辑器
    htmlEditor = $('.summernote').summernote({
        lang: 'zh-CN',
        height: 340,
        placeholder: '写点儿什么吧...',
        //上传图片的接口
        callbacks: {
            onImageUpload: function (files) {
                var data = new FormData();
                data.append('file', files[0]);
                data.append('token', token);
                data.append('key', "blog_image/" + files[0].name);
                tale.showLoading();
                $.ajax({
                    url: 'http://upload.qiniu.com/',     //上传图片请求的路径
                    method: 'POST',            //方法
                    data: data,                 //数据
                    processData: false,        //告诉jQuery不要加工数据
                    dataType: 'json',
                    contentType: false,        //<code class="javascript comments"> 告诉jQuery,在request head里不要设置Content-Type
                    success: function (result) {
                        tale.hideLoading();
                        if (result && result.key) {
                            file_upload(result)
                            var url = $('#attach_url').val() + result.key;
                            console.log('url =>' + url);
                            htmlEditor.summernote('insertImage', url);
                        } else {
                            tale.alertError(result.msg || '图片上传失败');
                        }
                    },
                    error:function(){
                        tale.hideLoading();
                        tale.alertError('图片上传失败');
                    }
                });
            }
        }
    });

    var fmtType = $('#fmtType').val();
    // 富文本编辑器
    if (fmtType != 'markdown') {
        var this_ = $('#switch-btn');
        mditor.value = '';
        $('#md-container').hide();
        $('#html-container').show();
        this_.text('切换为Markdown编辑器');
        this_.attr('type', 'texteditor');
    } else {
        var this_ = $('#switch-btn');
        $('#html-container').hide();
        $('#md-container').show();
        $('#fmtType').val('markdown');
        this_.attr('type', 'markdown');
        this_.text('切换为富文本编辑器');
        htmlEditor.summernote("code", "");
    }

    /*
     * 切换编辑器
     * */
    $('#switch-btn').click(function () {
        var type = $('#fmtType').val();
        var this_ = $(this);
        if (type == 'markdown') {
            // 切换为富文本编辑器
            if ($('#md-container .markdown-body').html().length > 0) {
                $('#html-container .note-editable').empty().html($('#md-container .markdown-body').html());
                $('#html-container .note-placeholder').hide();

            }
            mditor.value = '';
            $('#md-container').hide();
            $('#html-container').show();
            this_.text('切换为Markdown编辑器');
            $('#fmtType').val('html');
        } else {
            // 切换为markdown编辑器
            if ($('#html-container .note-editable').html().length > 0) {
                mditor.value = '';
                mditor.value = toMarkdown($('#html-container .note-editable').html());
            }
            $('#html-container').hide();
            $('#md-container').show();
            $('#fmtType').val('markdown');
            this_.text('切换为富文本编辑器');
            htmlEditor.summernote("code", "");
        }
    });
    // Tags Input
    $('#tags').tagsInput({
        width: '100%',
        height: '35px',
        defaultText: '请输入文章标签'
    });

    // $("#multiple-sel").select2({
    //     width: '100%'
    // });



    // var thumbdropzone = $('.dropzone');
    //
    // // 缩略图上传
    // $("#dropzone").dropzone({
    //     url: "http://upload.qiniu.com/",
    //     filesizeBase: 1024,//定义字节算法 默认1000
    //     maxFilesize: '10', //MB
    //     fallback: function () {
    //         tale.alertError('暂不支持您的浏览器上传!');
    //     },
    //     acceptedFiles: 'image/*',
    //     dictFileTooBig: '您的文件超过10MB!',
    //     dictInvalidInputType: '不支持您上传的类型',
    //     init: function () {
    //         this.on('success', function (files, result) {
    //             console.log("upload success..");
    //             console.log(" result => " + result);
    //             if (result && result.success) {
    //                 var url = attach_url + result.payload[0].fkey;
    //                 console.log('url => ' + url);
    //                 thumbdropzone.css('background-image', 'url(' + url + ')');
    //                 thumbdropzone.css('background-size', 'cover');
    //                 $('.dz-image').hide();
    //                 $('#thumbImg').val(url);
    //             }
    //         });
    //         this.on('error', function (a, errorMessage, result) {
    //             if (!result.success && result.msg) {
    //                 tale.alertError(result.msg || '缩略图上传失败');
    //             }
    //         });
    //     }
    // });

});

/*
 * 自动保存为草稿
 * */
function autoSave() {
    var content = $('#fmtType').val() == 'markdown' ? mditor.value : htmlEditor.summernote('code');
    var title = $('#articleForm input[name=title]').val();
    if (title != '' && content != '') {
        $('#content-editor').val(content);
        $("#articleForm #categories").val($('#multiple-sel').val());
        var params = $("#articleForm").serialize();
        var url = $('#articleForm #cid').val() != '' ? '/xadmin/article/modify/' : '/xadmin/article/create/';
        tale.post({
            url: url,
            data: params,
            success: function (result) {
                if (result && result.success) {
                    $('#articleForm #cid').val(result.payload);
                } else {
                    tale.alertError(result.msg || '保存文章失败');
                }
            }
        });
    }
}

/**
 * 保存文章
 * @param status
 */
function subArticle(status) {
    var content = $('#fmtType').val() == 'markdown' ? mditor.value : htmlEditor.summernote('code');
    var title = $('#articleForm input[name=title]').val();
    if (title == '') {
        tale.alertWarn('请输入文章标题');
        return;
    }
    if (content == '') {
        tale.alertWarn('请输入文章内容');
        return;
    }
    clearInterval(refreshIntervalId);
    $('#content-editor').val(content);
    $("#articleForm #status").val(status);
    $("#articleForm #categories").val($('#multiple-sel').val());
    var params = $("#articleForm").serialize();
    var url = $('#articleForm #pk').val() != '' ? '/xadmin/article/modify/' : '/xadmin/article/modify/';
    tale.post({
        url: url,
        data: params,
        success: function (result) {
            if (result && result.success) {
                tale.alertOk({
                    text: '文章保存成功',
                    then: function () {
                        setTimeout(function () {
                            window.location.href = '/xadmin/article/';
                        }, 500);
                    }
                });
            } else {
                tale.alertError(result.msg || '保存文章失败');
            }
        }
    });
}


function file_upload(info) {
    tale.post({
        url: '/xadmin/attach/upload/',
        data: {
            csrfmiddlewaretoken: $('#csrf_token').val(),
            info: info
        },
        success: function (result) {
            if (result && result.success) {
                tale.alertOk('附件上传成功');
            } else {
                tale.alertError(result.msg || '数据库存储失败，请刷新文件列表');
            }
        }
    });
}
