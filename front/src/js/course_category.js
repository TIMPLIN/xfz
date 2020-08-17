function CourseCategory() {

}

CourseCategory.prototype.run = function () {
    var self = this;
    self.listenAddCategoryEvent();
    self.listenEditCategoryEvent();
    self.listenDeleteCategoryEvent();
};

CourseCategory.prototype.listenAddCategoryEvent = function () {
    var addBtn = $('#add-btn');
    addBtn.click(function () {
        xfzalert.alertOneInput({
            'title': '添加新闻分类',
            'placeholder': '输入新闻分类',
            'confirmCallback': function (inputValue) {
                xfzajax.post({
                    'url': '/cms/add_course_category/',
                    'data': {
                        'name': inputValue
                    },
                    'success': function (result) {
                        if(result['code'] === 200){
                            window.location.reload();
                        }else{
                            xfzalert.close();
                        }
                    }
                });
            }
        });
    })
};


CourseCategory.prototype.listenDeleteCategoryEvent = function () {
    var deleteBtn = $('.delete-btn');
    deleteBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr('data-pk');
        xfzalert.alertConfirm({
            'title': '确定删除该分类吗?',
            'confirmCallback': function () {
                xfzajax.post({
                    'url': '/cms/delete_course_category/',
                    'data': {
                        'course_id': pk
                    },
                    'success': function (result) {
                        if(result['code'] === 200){
                            window.location.reload();
                        }else{
                            xfzalert.close();
                        }
                    }
                });
            }
        });
    });
};


CourseCategory.prototype.listenEditCategoryEvent = function () {
    var editBtn = $('.edit-btn');
    editBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr('data-pk');
        var name = tr.attr('data-name');
        xfzalert.alertOneInput({
            'title': '修改分类名称',
            'placeholder': '输入新的新闻分类',
            'value': name,
            'confirmCallback': function (inputValue) {
                xfzajax.post({
                    'url': '/cms/edit_course_category/',
                    'data': {
                        'pk': pk,
                        'name': inputValue
                    },
                    'success': function (result) {
                        if(result['code'] === 200){
                            window.location.reload();
                        }else{
                            xfzalert.close();
                        }
                    }
                });
            }
        });
    });
};

$(function () {
    var category = new CourseCategory();
    category.run();
});