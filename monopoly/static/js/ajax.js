function request_del_pc(pk) {
    $.ajax({
        url: "pc/delete/"+ pk +"/",
        data: {
            'pk': pk
        },
        processData: false,
        contentType: false,
        type: 'GET',
        success: function(data){
            var pc = document.querySelector("#pc-" + pk);
            pc.remove()
        }
    });
}

function request_add_pc() {

    var formElement = document.querySelector("#formPc");
    var formData = new FormData(formElement);

    $.ajax({
        url: "pc/",
        data: formData,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(data){
            select_last_pc(formData.get("name"))
        }
    });
}

function select_last_pc(name){
    $.ajax({
        url: "pc/ajax/select_last_pc/",
        processData: false,
        contentType: false,
        type: 'GET',
        success: function(data){
            pc = []

            JSON.parse(data, function(tables, data) {
                pc.push(data)
            });
            
            pc.splice(0, 1)
            pc.splice(4, 6)

            if (name == "") {add_pc(null)}
            else add_pc(pc)
        }
    });

    function add_pc(pc){
        if (pc == null){ return }

        let row = document.getElementById("row-pc");

        row.innerHTML += `<div class="col-lg-3 col-5 mt-2 mb-2  animate__animated animate__fadeIn" id="pc-`+ pc[0] + `">
            <div class="card text-white bg-dark mb-3 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">` + pc[1] + `</h5>
                    <h6 class="card-subtitle mb-2 text-muted">ip : ` + pc[2] + `</h6>
                    <h6 class="card-subtitle mb-2 text-muted">mac_adress : ` + pc[3] + `</h6>
                    <div class="mt-3 mb-2 ">
                        <a href="pc/`+ pc[0] + `/" class="btn btn-light text-weight-buttons">Посмотреть</a>
                        <a class="btn btn-danger text-weight-buttons" onclick="request_del_pc(`+ pc[0] + `)">Удалить</a>
                    </div>
                </div>
            </div>
        </div>`
    }
}