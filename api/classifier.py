import sqlite3


def __with_db_context(db_path, fn):    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    result = fn(cursor)
    cursor.close()
    conn.close()
    return result


# Dataset yang digunakan adalah dari tahun 2019 dan 2020
def __get_past_dataset(cursor):
    cursor.execute('''
        SELECT
            keketatan, nilai, rank_angkatan, pendaftar_diterima
        FROM
            JurusanPerTahun
        JOIN
            Pendaftaran ON Pendaftaran.pilihan = JurusanPerTahun.id
        WHERE tahun < 2021;
        '''
    )
    return cursor.fetchall()


class DiscreteDataset:

    def __init__(self, dataset, result_index, modified_attrs_min, modified_attrs_max, class_count):
        self.dataset = dataset
        self.result_index = result_index
        self.class_count = class_count
        self.modified_attrs = {
            'min': modified_attrs_min,
            'max': modified_attrs_max
        }

        self.total_data = len(self.dataset)
        self.total_accepted_count = 0
        self.total_rejected_count = 0
        for data in self.dataset:
            if data[self.result_index] == 1:
                self.total_accepted_count += 1
            else:
                self.total_rejected_count += 1
    
    def classify(self, raw_data):
        data_dimension = len(self.dataset[0])
        if len(raw_data) != data_dimension - 1:
            raise Exception(f'expecting data to have {data_dimension - 1} attributes')

        # ubah ke diskrit
        temp_list = []
        for i, attr in enumerate(raw_data):
            new = attr
            if i in self.modified_attrs['min']:
                new = DiscreteDataset.__classify(
                    attr,
                    self.modified_attrs['min'][i],
                    self.modified_attrs['max'][i],
                    self.class_count
                )
            temp_list.append(new)
        data = tuple(temp_list)

        percentage_accepted = 1
        percentage_rejected = 1
        for i, attr in enumerate(data):
            acc, rej = self.__calculate_weight(i, attr)
            percentage_accepted *= acc
            percentage_rejected *= rej

        weight_accept = percentage_accepted * (self.total_accepted_count / self.total_data)
        weight_reject = percentage_rejected * (self.total_rejected_count / self.total_data)

        return 1 if weight_accept >= weight_reject else 0 

    # Menerima list dari tuple yang berisikan dataset beserta
    # index dari atribut data yang ingin diubah (index tuple).
    #
    # Kemudian fungsi ini akan mengubah atribut-atribut tersebut
    # menjadi nilai diskrit.
    @classmethod
    def from_dataset(cls, raw_dataset, indexes, result_index, class_count = 5):
        # Mencari nilai tertinggi dan terendah untuk masing-masing
        # atribut yang dipilih
        attrs_max = {}
        attrs_min = {}
        for i in indexes:
            attrs_max[i] = -99999
            attrs_min[i] = 99999
        for data in raw_dataset:
            for i in indexes:
                attrs_max[i] = data[i] if attrs_max[i] < data[i] else attrs_max[i]
                attrs_min[i] = data[i] if attrs_min[i] > data[i] else attrs_min[i]
        
        # Klasifikasi
        new_dataset = []
        for data in raw_dataset:
            temp_list = []
            for i in range(len(data)):
                if i in indexes:
                    new_data = DiscreteDataset.__classify(
                        data[i],
                        attrs_min[i],
                        attrs_max[i],
                        class_count
                    )
                    temp_list.append(new_data)
                # jika bukan atribut yang perlu diubah, jangan
                # lakukan apa-apa
                else:
                    temp_list.append(data[i])
            new_tuple = tuple(temp_list)
            new_dataset.append(new_tuple)

        return cls(new_dataset, result_index, attrs_min, attrs_max, class_count)

    def __calculate_weight(self, index, value):
        accepted_count = 0
        rejected_count = 0
        for data in self.dataset:
            if data[index] == value:
                if data[self.result_index] == 1:
                    accepted_count += 1
                else:
                    rejected_count += 1
        return accepted_count / self.total_accepted_count, \
                rejected_count / self.total_rejected_count

    @staticmethod
    def __classify(value, min_val, max_val, class_count):
        class_range = (max_val - min_val) / class_count
        for i in range(class_count):
            if value < min_val + class_range * (i + 1):
                return i + 1
        return class_count


raw_past_dataset = __with_db_context('data-snmptn.db', __get_past_dataset)
past_dataset = DiscreteDataset.from_dataset(raw_past_dataset, [0, 1, 2], 3)


# Public API dari classifier.
#
# Parameter dataset berupa list/tuple yang urutan elemennya
# seperti berikut:
#       keketatan, nilai rata-rata, rank angkatan
def classify(data):
    return past_dataset.classify(data)
