CREATE TABLE Jurusan (
    id INTEGER PRIMARY KEY,
    nama VARCHAR(128) NOT NULL,
    universitas VARCHAR(128) NOT NULL,
    kuota INTEGER NOT NULL,
    peminat INTEGER NOT NULL,
    tahun INTEGER NOT NULL
);

CREATE TABLE HasilPendaftaran (
    id INTEGER PRIMARY KEY,
    deskripsi VARCHAR(32)
);

INSERT INTO HasilPendaftaran
VALUES
    (1, 'lolos di pilihan 1'),
    (2, 'lolos di pilihan 2'),
    (3, 'tidak lolos');

CREATE TABLE Siswa (
    id INTEGER PRIMARY KEY,
    rata_rata_rapot FLOAT NOT NULL,
    rangking INTEGER,
    pilihan_1 INTEGER,
    pilihan_2 INTEGER,
    hasil_pendaftaran INTEGER NOT NULL,
    tahun_angkatan INTEGER NOT NULL,

    FOREIGN KEY (pilihan_1) REFERENCES Jurusan(id),
    FOREIGN KEY (pilihan_2) REFERENCES Jurusan(id),
    FOREIGN KEY (hasil_pendaftaran) REFERENCES HasilPendaftaran(id)
);
