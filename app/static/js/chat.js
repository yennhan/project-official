$(document).ready(function(){
    var url=('http://' + document.domain + ':' + location.port);
    var socket = io.connect(url+'/dashboard');
    var chat_socket = io.connect(url+'/private_chat')
    var private_socket=io.connect(url+'/private')

    $('.anyClass').each(function () {
    $(this).scrollTop($(this)[0].scrollHeight);
});

    $('#load_history').on('click',function(){
    });
    chat_socket.on('chat_content_1',function(msg){
            console.log(msg);
            $('#chat_con').append("<div class='pd-t-5'></div><div class='pd-l-200 col-md-offset-3'><div class='mg-l-120 pd-l-100'><div class='rounded-left bg-primary pd-l-5 pd-t-5 pd-r-5 tx-white tx-hind tx-sm-normal'>"+msg[0]+"<div class='tx-right bg-primary tx-hind tx-gray bg-gray-200 tx-11'>"+msg[1]+"</div></div></div></div>");
            $('.anyClass').each(function () {
            $(this).scrollTop($(this)[0].scrollHeight);
});

    })
    chat_socket.on('chat_content_2',function(msg){
        console.log(msg);
        $('#chat_con').append("<div class='pd-t-5'></div><div class='pd-r-200 col-md-offset-3'><div class='mg-r-120 pd-r-100'><div class=' rounded-right bg-gray-700 pd-r-5 pd-l-5 pd-t-5 tx-left tx-hind tx-white tx-sm-normal'>"+msg[0]+"<div class='tx-hind tx-gray bg-gray-700 pull-right tx-11'>"+msg[1]+"</div></div></div></div>");
            $('.anyClass').each(function () {
            $(this).scrollTop($(this)[0].scrollHeight);
});
    })

    $('#send_button').on('click',function(){
        chat_socket.emit('chat_message',$('#send_message').val());
        $('#send_message').val('');
    });

    $('#send_username').on('click',function(){
        private_socket.emit('username',$('#username').val());
    });

    $('#send_private_message').on('click',function(){
        var recipient = $('#send_to_username').val();
        var message_to_send = $('#private_message').val();
        private_socket.emit('private_message',{'username':recipient,'message':message_to_send});
    });

    private_socket.on('new_private_message',function(msg){
        console.log(msg);
    });
    socket.on('connect',function(){
    });
});