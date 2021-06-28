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
     * Menjalankan kalkulasi prediksi di server. Lakukan sinkronisasi
     * di caller.
     */
    function fetchPrediction(nilai, rank, universitas, jurusan) {
        const url = 'http://localhost:8000/calculate'
                    + `?nilai=${nilai}`
                    + `&rank=${rank}`
                    + `&universitas=${universitas}`
                    + `&jurusan=${jurusan}`

        return (async () => {
            const res = await fetch(url)
            const data = await res.json()
            return data['result']
        })()
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


    /**
     * Melakukan validasi ke field rank angkatan.
     *
     * Return [nilai, errorMsg]
     */
    function validateRankAngkatan() {
        const val = $('#rank-angkatan').val().trim()

        if (val === '') {
            return [null, 'field tidak boleh kosong']
        } else if (!Number.isInteger(Number(val))) {
            return [null, 'field hanya dapat diisi bilangan bulat positif']
        } else if (Number(val) < 0) {
            return [null, 'angka yang dimasukkan tidak boleh bernilai negatif']
        }

        return [Number(val), null]
    }


    $('#main-form').submit(function(event) {
        $('#mean-rapot-err').addClass('d-none')
        $('#rank-angkatan-err').addClass('d-none')

        const [mean, meanErrMsg] = validateMeanRapot()
        if (meanErrMsg) {
            $('#mean-rapot-err').html(`* ${meanErrMsg}`)
            $('#mean-rapot-err').removeClass('d-none')

            event.preventDefault()
            return
        }

        const [rank, rankErrMsg] = validateRankAngkatan()
        if (rankErrMsg) {
            $('#rank-angkatan-err').html(`* ${rankErrMsg}`)
            $('#rank-angkatan-err').removeClass('d-none')

            event.preventDefault()
            return
        }

        event.preventDefault()

        const pilihan1 = {
            universitas: $('.universitas-1').val(),
            jurusan: $('.jurusan-1').val()
        }
        const pilihan2 = {
            universitas: $('.universitas-2').val(),
            jurusan: $('.jurusan-2').val()
        }

        Promise.all([
            fetchPrediction(mean, rank, pilihan1.universitas, pilihan1.jurusan),
            fetchPrediction(mean, rank, pilihan2.universitas, pilihan2.jurusan),
        ])
        .then(results => {
            displayResults(results)

            $('#submit').prop('disabled', false)
            $('#submit-loading').addClass('d-none')
        })

        $('#submit').prop('disabled', true)
        $('#submit-loading').removeClass('d-none')
    });


    function displayResults(results) {
        const layout = $('#result-layout').html()
        $('#result-container').html(layout)

        const acc = $('#result-accepted').html()
        const rej = $('#result-rejected').html()

        $('#result-container #result-pilihan-1').append(
            results[0] === 'DITERIMA'? acc : rej
        );
        $('#result-container #result-pilihan-2').append(
            results[1] === 'DITERIMA'? acc : rej
        );
    }
})