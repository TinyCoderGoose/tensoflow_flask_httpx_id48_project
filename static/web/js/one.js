var datacountall = 1;
var keywordall='显卡';
$(function () {
    function allBtn(){
        if($('#cbjd').attr('value')==='0' && $('#cbtb').attr('value')==='0' && $('#cbsn').attr('value')==='0'){
            $('.Complete').addClass('Completeon')
            $('.Complete').removeClass('Complete')
        }
    }
    $('.Complete').click(function () {
        $('.Complete').addClass('Completeon')
        $('.Complete').removeClass('Complete')
    });
    $('#asc').click(function () {
        $('#asc').addClass('on')
        $('#asc').siblings('a').removeClass('on')
        get_datas(keywordall,1)
    });
    $('#desc').click(function () {
        $('#desc').addClass('on')
        $('#desc').siblings('a').removeClass('on')
        get_datas(keywordall,1)
    });
    $('#default').click(function () {
        $('#default').addClass('on')
        $('#default').siblings('a').removeClass('on')
        get_datas(keywordall,1)
    });
    $('#cbtb').click(function () {
        if($('#cbtb').attr('value')==='0'){
            document.getElementById('cbtb').value='1'
            $('.Completeon').addClass('Complete')
            $('.Complete').removeClass('Completeon')
        }else{
            document.getElementById('cbtb').value='0'
            allBtn()
        }
        get_datas(keywordall,1)
    });
    $('#cbjd').click(function () {
        if($('#cbjd').attr('value')==='0'){
            document.getElementById('cbjd').value='1'
            $('.Completeon').addClass('Complete')
            $('.Complete').removeClass('Completeon')
        }else{
            document.getElementById('cbjd').value='0'
            allBtn()
        }
        get_datas(keywordall,1)
    });
    $('#cbsn').click(function () {
        if($('#cbsn').attr('value')==='0'){
            document.getElementById('cbsn').value='1'
            $('.Completeon').addClass('Complete')
            $('.Complete').removeClass('Completeon')
        }else{
            document.getElementById('cbsn').value='0'
            allBtn()
        }
        get_datas(keywordall,1)
    });
    $('#next_page').click(function () {
        var next = parseInt(document.getElementById('current_page').text);
        if (datacountall===0){
             $('#page_count').html("总页数：1");
        }else{
             $('#page_count').html("总页数："+datacountall);
        }

        if (next>=datacountall){
            alert("已经走到尽头啦")
        }else{
            $('#current_page').html(next+1)
            get_datas(keywod=keywordall,page=next+1)
        }
    });
    $('#last_page').click(function () {
        var last = parseInt(document.getElementById('current_page').text);
        $('#page_count').html("总页数："+datacountall);
        if (last<=1){
            alert("前面没有路啦")
        }else{
            $('#current_page').html(last-1)
            get_datas(keywod=keywordall,page=last-1)
        }
    });

    get_datas()
    $('.hotword a').click(function () {
        var searchtext = document.getElementById('searchName');
        searchtext.value = this.text;
        get_datas(this.text)
    })
    function search(){
        var keyword = document.getElementById('searchName').value;
        get_datas(keyword,1)
        keywordall=keyword
    }
    $('.Search_btn').click(function () {
        search()
    })
    $('#searchName').keypress(function () {
        if(event.keyCode == 13){
            search()
        }
    })
})