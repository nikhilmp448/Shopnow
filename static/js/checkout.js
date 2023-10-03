$(document).ready(function () {

    $(".rzp").click(function (e) { 
        e.preventDefault();

        var full_name = $("[name='full_name']").val();
        var mobile = $("[name='mobile']").val();
        var address = $("[name='address']").val();
        var country = $("[name='country']").val();
        var state = $("[name='state']").val();
        var city = $("[name='city']").val();
        var landmark = $("[name='landmark']").val();
        var pin_code = $("[name='pin_code']").val();
        var email = $("[name='email']").val();
        var username = $("[name='username']").val();
        var token = $("input[name= 'csrfmiddlewaretoken']").val();

        if (full_name==""||mobile==""||address==""||country==""||state==""||city==""||landmark==""||pin_code=="")

        {
          
            swal("Alert!", "All fields are mandatoty!", "error");
            return false;
        }
        else
        {   

            $.ajax({
                method: "GET",
                url: "/proceed_to_pay",
                
                success: function (response) {
                    // console.log(response);
                    var options = {
                        "key": "rzp_test_gI5wxfxo3on80w", // Enter the Key ID generated from the Dashboard
                        "amount": response.total_price * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name": "ShopNow pvt.ltd",
                        "description": "Thank you for buying from us",
                        "image": "https://example.com/your_logo",
                        // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        // "callback_url": "https://eneqd3r9zrjok.x.pipedream.net/",
                        "handler": function (responseb){
                            // console.log(responseb);
                            //  alert(responseb.razorpay_payment_id);


                            data = {
                                "full_name": full_name,
                                "mobile": mobile,
                                "address": address,
                                "country": country,
                                "state": state,
                                "city": city,
                                "landmark": landmark,
                                "pin_code": pin_code,
                                "payment_mode":"Razorpay",
                                "payment_id":responseb.razorpay_payment_id,
                                csrfmiddlewaretoken : token
                            }


                            $.ajax({
                                method: "POST",
                                url: "/placeorder",
                                data: data,
                                
                                success: function (responsec) {
                    
                                    swal("congratulations!", responsec.status , "success").then((value) => {
                                        window.location.href= '/orderdisplay'
                                      });
                                   
                                }
                            });
                            
                        },
                        "prefill": {
                            "name": username,
                            "email": email,
                            "contact": mobile
                        },
                        "notes": {
                            "address": "Razorpay Corporate Office"
                        },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.on('payment.failed', function (response){
                        console.log(response);
                        swal({
                            title:response.error.description,
                            icon: 'error'
                        })
                            // alert(response.error.code);
                            // alert(response.error.description);
                            // alert(response.error.source);
                            // alert(response.error.step);
                            // alert(response.error.reason);
                            // alert(response.error.metadata.order_id);
                            // alert(response.error.metadata.payment_id);
                    });
            
                    rzp1.open();
                }
            });


            

        }

    });
    
});