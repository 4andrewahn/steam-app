$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    $('#game-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const gameID = button.data('source') // Extract info from data-* attributes
        const content = button.data('content') // Extract info from data-* attributes

        const modal = $(this)
        if (gameID === 'New Game') {
            modal.find('.modal-title').text(gameID)
            $('#game-form-display').removeAttr('gameID')
        } else {
            modal.find('.modal-title').text('Edit Game' + gameID)
            $('#game-form-display').attr('gameID', gameID)
        }

        if (content) {
            modal.find('.form-control').val(content);
        } else {
            modal.find('.form-control').val('');
        }
    })

    $('#submit-game').click(function () {
        const gID = $('#game-form-display').attr('gameID');
        console.log($('#game-modal').find('.form-control').val())
        $.ajax({
            type: 'POST',
            url: gID ? '/edit/' + gID : '/create',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'name': $('#game-modal').find('.form-control').val()
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.search').click(function () {
        const searchword = document.getElementById("search-bar").value;
        $.ajax({
            type: 'POST',
            url: '/search/' + searchword,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'data': searchword
            }),
            success: function (res) {
                window.location.href = '/search/' + searchword;
                console.log(res.response)
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.remove').click(function () {
        const remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });
});