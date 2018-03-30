$(document).ready(function(){

  //Register form Handler
  var registerForm = $('.register-form')
  var registerFormMethod = registerForm.attr('method')
  var registerFormEndPoint = registerForm.attr('action')

  function displaySubmitting(submitBtn, defaultText, doSubmit){
    if (doSubmit){
      submitBtn.addClass('disabled')
      submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending..")
    }else{
      submitBtn.removeClass('disabled')
      submitBtn.html(defaultText)
    }
  }

  registerForm.submit(function(event){
    event.preventDefault()
    var registerFormSubmitBtn = registerForm.find("[type='submit']")
    var registerFormSubmitBtnTxt = registerFormSubmitBtn.text()
    var registerFormData = registerForm.serialize()
    console.log(registerFormData)
    var thisForm = $(this)
    displaySubmitting(registerFormSubmitBtn, '', true)
    $.ajax({
      method: registerFormMethod,
      url : registerFormEndPoint,
      data: registerFormData,
      success: function(data){
        thisForm[0].reset()
        $.alert({
          title: 'Success',
          content: 'You have been registered',
          theme: 'modern',
        })
        setTimeout(function(){
          displaySubmitting(registerFormSubmitBtn, registerFormSubmitBtnTxt, false)
        }, 2000)
      },
      error: function(error){
        var jsonData = error.responseJSON
        var msg=""

        $.each(jsonData, function(key, value){
          msg += key + " : " + value[0].message + '</br>'
        })

        $.alert({
          title: 'Oops',
          content: msg,
          theme: 'modern',
        })

        setTimeout(function(){
          displaySubmitting(registerFormSubmitBtn, registerFormSubmitBtnTxt, false)
        }, 2000)
      }
    })
  })

  //Contact form Handler
  var contactForm = $('.contact-form')
  var contactFormMethod = contactForm.attr('method')
  var contactFormEndPoint = contactForm.attr('action')

  function displaySubmitting(submitBtn, defaultText, doSubmit){
    if (doSubmit){
      submitBtn.addClass('disabled')
      submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending..")
    }else{
      submitBtn.removeClass('disabled')
      submitBtn.html(defaultText)
    }
  }

  contactForm.submit(function(event){
    event.preventDefault()
    var contactFormSubmitBtn = contactForm.find("[type='submit']")
    var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()
    var contactFormData = contactForm.serialize()
    var thisForm = $(this)
    displaySubmitting(contactFormSubmitBtn, '', true)
    $.ajax({
      method: contactFormMethod,
      url : contactFormEndPoint,
      data: contactFormData,
      success: function(data){
        thisForm[0].reset()
        $.alert({
          title: 'Success',
          content: 'Your Response has been Recorded',
          theme: 'modern',
        })
        setTimeout(function(){
          displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
        }, 2000)
      },
      error: function(error){
        var jsonData = error.responseJSON
        var msg=""

        $.each(jsonData, function(key, value){
          msg += key + " : " + value[0].message + '</br>'
        })

        $.alert({
          title: 'Oops',
          content: msg,
          theme: 'modern',
        })

        setTimeout(function(){
          displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
        }, 2000)
      }
    })
  })


  //AutoSearch
  var searchForm = $('.search-form')
  var searchInput = searchForm.find("[name='q']")
  var  typingTimer;
  var typingInterval = 1500 //1.5 secs
  var searchBtn = searchForm.find("[type='submit']")
  searchInput.keyup(function(event){
    //key released
    clearTimeout(typingInterval)
    typingTimer = setTimeout(performSearch, typingInterval)
  })
  searchInput.keydown(function(event){
    //key pressed
    clearTimeout(typingInterval)
  })

  function displaySearching(){
    searchBtn.addClass('disabled')
    searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching..")
  }

  function performSearch(){
    displaySearching()
    var query = searchInput.val()
    setTimeout(function(){
      window.location.href = '/search/?q=' + query
    }, 1000)

  }

  //Add To Cart and Remove
  var productForm = $('.form-product-ajax')
  productForm.submit(function(event){
    event.preventDefault();
    var thisForm = $(this);
    var actionEndpoint = thisForm.attr('data-endpoint');
    var httpMethod = thisForm.attr('method');
    var formData = thisForm.serialize();

    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function(data){
        var submitSpan = thisForm.find('.submit-span')
        if (data.added){
          submitSpan.html("<div class='btn-group' role='group'> <a class='btn btn-success' href='/cart/'><i class='fas fa-check'></i> In cart</a> <button type='submit' class='btn btn-outline-danger'><i class='fas fa-times'></i> Remove?</button></div>")
        }else {
          submitSpan.html("<button type='submit' class='btn btn-block btn-primary'>Add to cart <i class='fas fa-cart-plus'></i></button>")
        }
        var navbarCount = $('.navbar-cart-count')
        navbarCount.text(data.cartItemCount)
        var currentPath = window.location.href
        if (currentPath.indexOf('cart') != -1){
          refreshCart()
        }
      },
      error: function(errorData){
        $.alert({
          title: "Oops",
          content: "An error occured",
          theme: "light",
        })
        }

    })

  })

    function refreshCart(){
        var cartTable = $('.cart-table');
        var cartBody = cartTable.find('.cart-body');
        var productRows = cartBody.find('.cart-product');
        var currentUrl = window.location.href;
        var refreshCartUrl = '/api/cart/';
        var refreshCartMethod = 'GET';
        var data = {};
        $.ajax({
          url: refreshCartUrl,
          method: refreshCartMethod,
          data: data,
          success: function(data){
            var hiddenCartItemRemoveForm = $('.cart-item-remove-form')
            if (data.products.length > 0){
              productRows.html(" ");
              i=data.products.length
              $.each(data.products, function(index, value){
                var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                newCartItemRemove.css("display","block")
                newCartItemRemove.find('.cart-item-product-id').val(value.id)
                var str = "<tr><th scope=\"row\">" + i + "</th><td><a href='" + value.url + "'>" + value.title + "</a>" + newCartItemRemove.html() + "</td><td>" + value.price + "</td></tr>";
                cartBody.prepend(str)
                i--
              })
              cartBody.find('.cart-subtotal').text(data.subtotal)
              cartBody.find('.cart-total').text(data.total)
            }else{
              window.location.href = currentUrl
            }
          },
          error: function(errorData){
            $.alert({
            title: "Oops!",
            content: "An error occurred",
            theme: "modern",
          })
          }
        })
    }
})
