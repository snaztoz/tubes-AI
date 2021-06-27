CREATE TABLE Jurusan (
    id INTEGER PRIMARY KEY,
    pt VARCHAR(8) NOT NULL,
    jurusan_fakultas VARCHAR(32) NOT NULL,

    UNIQUE(pt, jurusan_fakultas)
);

CREATE TABLE JurusanPerTahun (
    id INTEGER PRIMARY KEY,
    id_jurusan INTEGER NOT NULL,
    tahun INTEGER NOT NULL,
    keketatan DECIMAL(9, 9) NOT NULL,

    UNIQUE(id_jurusan, tahun),
    FOREIGN KEY (id_jurusan) REFERENCES Jurusan(id)
);

CREATE TABLE Pendaftaran (
    id_pendaftar VARCHAR(9) PRIMARY KEY,
    nilai DECIMAL(6, 4) NOT NULL,
    pilihan INTEGER NOT NULL,
    pendaftar_diterima INTEGER NOT NULL,

    FOREIGN KEY (pilihan) REFERENCES JurusanPerTahun(id)
);
