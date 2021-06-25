$(document).ready(function() {

    $('#link-to-form').click(function(event) {
        event.preventDefault()
        $('#mean-rapot').focus()
    });


    async function fetchUniversitas() {
        const res = await fetch('http://localhost:8000/list-universitas')
        const data = await res.json()

        return data['list-universitas']
    }


    async function fetchJurusan(universitas) {
        const url = `http://localhost:8000/list-jurusan?universitas=${universitas}`

        const res = await fetch(url)
        const data = await res.json()

        return data['list-jurusan']
    }


    /**
     * Init fetch ketika page baru pertama kali load.
     */
    (async function() {
        const listUniversitas = await fetchUniversitas()

        listUniversitas.forEach(universitas => {
            $('.universitas').append(`<option value="${universitas}">${universitas}</option>`)
        })
        $('.universitas').removeAttr('disabled')

        const listJurusan = await fetchJurusan(listUniversitas[0])

        listJurusan.forEach(jurusan => {
            $('.jurusan').append(`<option value="${jurusan}">${jurusan}</option>`)
        })
        $('.jurusan').removeAttr('disabled')
    })();


    /**
     * Ketika value dari input universitas berubah, reload list
     * jurusan yang ada sesuai dengan value universitas yang baru.
     */
    $('.universitas').change(async function() {
        const which = $(this).attr('class').includes('universitas-1')
                        ? '1'
                        : '2'
        const universitas = $(this).val()

        const listJurusan = await fetchJurusan(universitas)

        $(`.jurusan-${which}`).empty()

        listJurusan.forEach(jurusan => {
            $(`.jurusan-${which}`).append(`<option value="${jurusan}">${jurusan}</option>`)
        })
    });


    /**
     * Melakukan validasi ke field mean rapot.
     *
     * Return [nilai, errorMsg]
     */
    function validateMeanRapot() {
        const val = $('#mean-rapot').val().trim()

        if (val === '') {
            return [null, 'field tidak boleh kosong']
        } else if (isNaN(val)) {
            return [null, 'field hanya dapat diisi angka']
        } else if (Number(val) < 0) {
            return [null, 'angka yang dimasukkan tidak boleh bernilai negatif']
        }

        return [Number(val), null]
    }


    $('#main-form').submit(function(event) {
        $('#mean-rapot-err').addClass('d-none')

        const [mean, errMsg] = validateMeanRapot()
        if (errMsg) {
            $('#mean-rapot-err').html(`* ${errMsg}`)
            $('#mean-rapot-err').removeClass('d-none')

            event.preventDefault()
            return
        }

        // TODO: fetch result ke API
        event.preventDefault()
        console.log(mean)
    });
})