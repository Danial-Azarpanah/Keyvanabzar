function AddToCart(id) {
    $.ajax({
        url: `/cart-add/${id}`,
        type: 'POST',
        data: {
            quantity: $('#quantity').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function () {
            Swal.fire({
                text: 'این محصول به سبد خرید شما اضافه شد',
                icon: 'success',
                confirmButtonText: 'باشه',
                showConfirmButton: false,
                timer: 1500
            }).then(function () {
                location.reload()
            })
        }

    });
}

function AddCompare(id) {
    $.get(`/add-comparison/${id}`).then(response => {
        if (response['error']) {
            Swal.fire({
                position: 'top-end-right',
                icon: 'warning',
                text: response['error'],
                showConfirmButton: false,
                confirmButtonColor: '#112031',
                timer: 1500
            })
        } else {
            Swal.fire({
                position: 'top-end-right',
                icon: 'success',
                text: 'این محصول به لیست مقایسه اضافه شد',
                showConfirmButton: false,
                confirmButtonColor: '#112031',
                timer: 1500
            })
        }
    })
}

function AddFavorite(id) {
    $.get(`/add-favorite/${id}`).then(response => {
        if (response['response'] === 'deleted') {
            Swal.fire({
                position: 'top-end-right',
                icon: 'success',
                text: 'این محصول از علاقه مندی‌های شما حذف شد',
                showConfirmButton: false,
                confirmButtonColor: '#112031',
                timer: 1500
            }).then(function () {
                location.reload()
            })
        } else {
            Swal.fire({
                position: 'top-end-right',
                icon: 'success',
                text: 'این محصول به علاقه مندی های شما اضافه شد',
                showConfirmButton: false,
                confirmButtonColor: '#112031',
                timer: 1500
            }).then(function () {
                location.reload()
            })
        }
    })
}

function CartDel(id) {
    Swal.fire({
        title: 'هشدار!!',
        text: 'آیااز حذف اطمینان دارید؟',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#FEBD17',
        cancelButtonColor: '#1A1A1A',
        cancelButtonText: 'خیر',
        confirmButtonText: 'بله',

    }).then((result) => {
        if (result.isConfirmed) {
            $.get(`/cart-del/${id}`).then(response => {
                Swal.fire({
                    text: 'عملیات با موفقیت انجام شد',
                    icon: 'success',
                    showConfirmButton: false,
                    timer: 1500
                }).then(function () {
                    location.reload();
                })

            })
        }

    })
}

$(document).on('submit', '#contactus-form', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/contact-us',
        data: {
            fullname: $('#fullname').val(),
            email: $('#email').val(),
            subject: $('#subject').val(),
            message: $('#message').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function () {
            Swal.fire({
                title: 'عملیات با موفقیت انجام شد',
                text: 'پیام شما با موفقیت ارسال گردید',
                icon: 'success',
                confirmButtonText: 'باشه',
                confirmButtonColor: '#FEBD17',
            }).then(function () {
                location.href = "{% url 'home:home' %}";
            })
        }

    })
})

function reply(id) {
    document.getElementById("parent-id").value = id;
    document.getElementById("review_comment").placeholder = "پاسخ خود را بنویسید"
    document.getElementById("scroll-point").scrollIntoView();
}

// Get a reference to the form and input elements
const form = document.getElementById('price-form');
const input = document.getElementById('amount');

// Add a listener for the form submission event
form.addEventListener('submit', (event) => {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Get the current URL and parse it into its parts
    const url = new URL(window.location.href);

    // Set the value of the "text" parameter to the input value
    url.searchParams.set('price', input.value);

    // Redirect to the new URL
    window.location.href = url.toString();
});