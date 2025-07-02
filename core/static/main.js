$(document).ready(function() {
    $('#id_master').change(function() {
        const masterId = $(this).val();
        const $container = $('#servicesContainer');

        if (masterId) {
            const selectedServices = [];
            $container.find('input[type="checkbox"]:checked').each(function() {
                selectedServices.push($(this).val());
            });

            $container.html(`
                <div class="text-center py-4">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Загрузка...</span>
                    </div>
                    <p class="mt-2">Загрузка услуг...</p>
                </div>
            `);

            $.ajax({
                url: '/get-services/',
                type: 'GET',
                data: {
                    'master_id': masterId,
                    'selected_services[]': selectedServices
                },
                success: function(response) {
                    if (response.html) {
                        $container.html(`
                            <div class="row">
                                ${response.html}
                            </div>
                        `);
                    } else {
                        $container.html('<p class="text-muted">Нет доступных услуг</p>');
                    }
                },
                error: function(xhr, status, error) {
                    console.error("AJAX Error:", status, error);
                    $container.html(`
                        <div class="alert alert-danger">
                            Ошибка загрузки услуг. Пожалуйста, попробуйте еще раз.
                        </div>
                    `);
                }
            });
        } else {
            $container.html('<p class="text-muted">Сначала выберите мастера</p>');
        }
    });
});