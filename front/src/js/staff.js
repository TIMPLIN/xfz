function Staff() {

}


Staff.prototype.DeleteStaff = function () {
    var delete_staff = $('.submit-delete-staff');
    delete_staff.click(function () {
        var self = $(this);
        var staff_pk = self.attr('data-staff-pk');
        xfzalert.alertConfirm({
            'title': '确定删除该员工？',
            'confirmCallback': function () {
                xfzajax.post({
                    'url': '/cms/delete_staff/',
                    'data': {
                        'staff_pk': staff_pk
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


Staff.prototype.run = function () {
    var self = this;
    self.DeleteStaff();
};


$(function () {
    var staff = new Staff();
    staff.run();
});