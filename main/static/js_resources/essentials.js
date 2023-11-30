$(document).ready(function () {
    $("#in_pais").change(function () {
        var selectedPais = $(this).val();
        if (selectedPais !== "-1") {
            // Realiza una solicitud AJAX para obtener los departamentos de ese país
            $.ajax({
                url: '/get_departamentos/',  // Define la URL en tu aplicación Django
                method: 'GET',
                data: { pais_id: selectedPais },
                success: function (data) {
                    $("#in_departamento").empty();  // Limpia el campo de selección antes de agregar nuevas opciones
                    $.each(data, function (index, item) {
                        $("#in_departamento").append($('<option>', {
                            value: item.id,
                            text: item.description
                        }));
                    });
                }
            });
        }
    });

    $("#in_departamento").change(function () {
        var selectedDepartamento = $(this).val();
        if (selectedDepartamento !== "-1") {
            // Realiza una solicitud AJAX para obtener los municipios de ese departamento
            $.ajax({
                url: '/get_municipios/',  // Define la URL en tu aplicación Django
                method: 'GET',
                data: { departamento_id: selectedDepartamento },
                success: function (data) {
                    // Llena el campo de selección de municipios con los datos recibidos
                    $("#in_municipio").empty();  // Limpia el campo de selección antes de agregar nuevas opciones
                    $.each(data, function (index, item) {
                        $("#in_municipio").append($('<option>', {
                            value: item.id,
                            text: item.description
                        }));
                    });
                }
            });
        }
    });
    
});
