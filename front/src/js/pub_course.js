function Course() {

}

Course.prototype.run = function () {
    var self = this;
    //self.listenUploadFileEvent();
    self.listenQiniuUploadFileEvent();
    self.initUEditor();
    self.listenSubmitEvent();
};


Course.prototype.initUEditor = function () {
    window.ue = UE.getEditor('editor', {
        'serverUrl': '/ueditor/upload/'
        // 'initialFrameHeight': 400
    });
};


Course.prototype.listenSubmitEvent = function () {
    var submitBtn = $('#submit-course');
    submitBtn.click(function (event) {
        event.preventDefault();
        var btn = $(this);
        var pk = btn.attr('data-course-id');

        var title = $("input[name='title']").val();
        var category_id = $("select[name='category']").val();
        var teacher_id = $("select[name='teacher']").val();
        var video_url = $("input[name='video_url']").val();
        var cover_url = $("input[name='cover_url']").val();
        var profile = window.ue.getContent();
        var price = $("input[name='price']").val();
        var duration = $("input[name='duration']").val();

        var url = '';
        if(pk){
            url = '/cms/edit_course/';
        }else{
            url = '/cms/pub_course/';
        }

        xfzajax.post({
            'url': url,
            'data': {
                'title': title,
                'video_url' : video_url,
                'cover_url' : cover_url,
                'price': price,
                'duration': duration,
                'profile': profile,
                'pk': pk,
                'category': category_id,
                'teacher': teacher_id
            },
            'success': function (result) {
                if(result['code'] === 200){
                    if(pk) {
                        xfzalert.alertSuccess('课程编辑成功', function () {
                            window.location.reload();
                        });
                    }else{
                        xfzalert.alertSuccess('课程发布成功', function () {
                            window.location.reload();
                        })
                    }
                }
            }
        });
    });
};


Course.prototype.listenQiniuUploadFileEvent = function () {
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
                        'error': self.handleFileUploadError,
                        'complete': self.handleFileUploadComplete
                    });
                }
            }
        });
    });
};

Course.prototype.handleFileUploadProgress = function (response) {
    var total = response.total;
    var percent = total.percent;
    var percentText = percent.toFixed(0)+"%";
    var progressGroup = Course.progressGroup;
    progressGroup.show();
    var progressBar = $('.progress-bar');
    progressBar.css({'width': percentText});
    progressBar.text(percentText);
};

Course.prototype.handleFileUploadError = function (error) {
    window.messageBox.showError(error.message);
    var progressGroup = Course.progressGroup;
    progressGroup.hide();
    console.log(error.message);
};

Course.prototype.handleFileUploadComplete = function (response) {
    var progressGroup = Course.progressGroup;
    progressGroup.hide();

    var domain = '';
    var filename = response.key;
    var url = domain + filename;
    var thumbnailInput = $("input[name='thumbnail']");
    thumbnailInput.val(url);
};



Course.prototype.listenUploadFileEvent = function () {
    var uploadBtn = $('#thumbnail-btn');
    uploadBtn.change(function () {
        var file = uploadBtn[0].files[0];
        //var file = this.files[0];
        var formData = new FormData();
        formData.append('file', file);
        xfzajax.post({
            'url': '/cms/upload_file/',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if(result['code'] === 200){
                    var url = result['url'];
                    var thumbnailInput = $('#thumbnail-form');
                    thumbnailInput.val(url);
                }
            }
        })
    });
};


$(function () {
    var course = new Course();
    course.run();

    News.progressGroup = $('#progress-group');
});