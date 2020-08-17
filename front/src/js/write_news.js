function News() {

}


News.prototype.initUEditor = function () {
    window.ue = UE.getEditor('editor', {
        'serverUrl': '/ueditor/upload/',
        'initialFrameHeight': 400
    });
};



News.prototype.listenSubmitEvent = function () {
    var submitBtn = $('#submit-btn');
    submitBtn.click(function (event) {
        event.preventDefault();
        var btn = $(this);
        var pk = btn.attr('data-news-id');

        var title = $("input[name='title']").val();
        var category = $("select[name='category']").val();
        var desc = $("input[name='desc']").val();
        var thumbnail = $("input[name='thumbnail']").val();
        var content = window.ue.getContent();

        var url = '';
        if(pk){
            url = '/cms/edit_news/';
        }else{
            url = '/cms/write_news/';
        }

        xfzajax.post({
            'url': url,
            'data': {
                'title': title,
                'category': category,
                'desc': desc,
                'thumbnail': thumbnail,
                'content': content,
                'pk': pk
            },
            'success': function (result) {
                if(result['code'] === 200){
                    if(pk) {
                        xfzalert.alertSuccess('新闻编辑成功', function () {
                            window.location.reload();
                    });
                    }else{
                        xfzalert.alertSuccess('新闻发布成功', function () {
                            window.location.reload();
                        })
                    }
                }
            }
        });
    });
};


News.prototype.listenQiniuUploadFileEvent = function () {
    var self = this;
    var uploadBtn = $('#thumbnail-btn');
    uploadBtn.change(function () {
        var file = this.files[0];
        xfzajax.get({
            'url': '/cms/qntoken/',
            'success': function (result) {
                if(result['code'] === 200){
                    var token = result['data']['token'];
                    var key = (new Date()).getTime() + '.' + file.name.split('.')[1];
                    var putExtra = {
                        fname: key,
                        params: {},
                        mimeType: ['image/png', 'video/x-ms-wmv', 'image/jpeg', 'image/gif']
                    };
                    var config = {
                        useCdnDomain: true,
                        retryCount: 6,
                        region: qiniu.region.z0
                    };
                    var observable = qiniu.upload(file, key, token, putExtra, config);
                    observable.subscribe({
                        'next': self.handleFileUploadProgress,
                        'complete': self.handleFileUploadComplete,
                        'error': self.handleFileUploadError
                    });
                }
            }
        });
    });
};

News.prototype.handleFileUploadProgress = function (response) {
    var total = response.total;
    var percent = total.percent;
    var percentText = percent.toFixed(0)+"%";
    var progressGroup = News.progressGroup;
    progressGroup.show();
    var progressBar = $('.progress-bar');
    progressBar.css({'width': percentText});
    progressBar.text(percentText);
};

News.prototype.handleFileUploadError = function (error) {
    window.messageBox.showError(error.message);
    var progressGroup = News.progressGroup;
    progressGroup.hide();
    var progressBar = $('.progress-bar');
    progressBar.css({'width': 0+'%'});
    progressBar.text(0+'%');
    console.log(error.message);
};

News.prototype.handleFileUploadComplete = function (response) {
    var progressGroup = News.progressGroup;
    progressGroup.hide();
    var progressBar = $('.progress-bar');
    progressBar.css({'width': 0+"%"});
    progressBar.text(0+"%");

    var domain = '';
    var filename = response.key;
    var url = domain + filename;
    var thumbnailInput = $("input[name='thumbnail']");
    thumbnailInput.val(url);
};




News.prototype.listenUploadFileEvent = function () {
    var uploadBtn = $('#thumbnail-btn');
    uploadBtn.change(function () {
        var file = uploadBtn[0].files[0];
        var formData = new FormData();
        formData.append('file', file);
        xfzajax.post({
            'url': '/cms/upload_file/',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if(result['code'] === 200){
                    var url = result['data']['url'];
                    var thumbnailInput = $('#thumbnail-form');
                    thumbnailInput.val(url);
                }
            }
        });
    });
};


News.prototype.run = function () {
    var self = this;
    self.listenUploadFileEvent();
    //self.listenQiniuUploadFileEvent();
    self.initUEditor();
    //self.listenSubmitEvent();
};

$(function () {
    var news = new News();
    news.run();

    News.progressGroup = $('#progress-group');
});