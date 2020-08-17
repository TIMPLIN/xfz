function UserInfo() {

}


UserInfo.prototype.ListenSubmitUserInfo = function () {
    var submit = $('#submit-userinfo');
    submit.click(function () {
        var emailInput = $('#email-form');
        var companyInput = $('#company-form');
        var schoolInput = $('#school-form');
        var addressInput = $('#address-form');
        var signatureInput = $('#signature-form');

        var email = emailInput.val();
        var company = companyInput.val();
        var address = addressInput.val();
        var signature = signatureInput.val();
        var school = schoolInput.val();

        xfzajax.post({
            'url': '/account/userinfo/',
            'data': {
                'email': email,
                'school': school,
                'address': address,
                'signature': signature,
                'company': company
            },
            'success': function (result) {
                if(result['code'] === 200){
                    xfzalert.alertSuccess('信息完善成功!', function () {
                        window.location.reload();
                    })
                }
            }
        });
    });
};


UserInfo.prototype.run(function () {
    var self = this;
    self.ListenSubmitUserInfo();
});


$(function () {
    var userinfo = new UserInfo();
    userinfo.run();
});