from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import mysql.connector
import openpyxl

app = Flask(__name__)
CORS(app)

# Koneksi ke MySQL
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="hris"
)

# Model untuk tabel items
class Item:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Karyawan:
    def __init__(self,id,nik,nama_lengkap,tempatlahir,tgllahir,agama,alamat,nohp,golongandarah,status,photo):
        self.id =id
        self.nik =nik
        self.nama_lengkap =nama_lengkap
        self.tempatlahir =tempatlahir
        self.tgllahir =tgllahir
        self.agama =agama
        self.alamat =alamat
        self.nohp =nohp
        self.golongandarah =golongandarah
        self.status =status
        self.photo =photo


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    nik = data.get('nik')
    print(nik)
    cursor = db.cursor()
    query = "SELECT * FROM tblkaryawan WHERE nik = %s"
    cursor.execute(query, (nik,))
    result = cursor.fetchone()
    print(query)
    print(result)

    if result is not None:
      # NIK exists, return success
      karyawan = Karyawan(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9], result[10])
      return jsonify({'success': True, 'data': karyawan.__dict__})
    else:
      # NIK does not exist, return failure
      return jsonify({'success': False})

@app.route('/updatedata', methods=['PUT'])
def updatedata():
    updated_data = request.json
    print(updated_data['nik']) 

    cursor = db.cursor()
    update_query = "UPDATE tblkaryawan SET nama_lengkap = %s, tempatlahir = %s , tgllahir = %s, agama = %s, alamat = %s, nohp = %s, golongandarah = %s, status = %s, photo = %s WHERE nik = %s"
    values = (updated_data['nama_lengkap'], updated_data['tempatlahir'],updated_data['tgllahir'],updated_data['agama'],updated_data['alamat'],updated_data['nohp'],updated_data['golongandarah'],updated_data['status'],updated_data['photo'], updated_data['nik'])
    print(update_query, values)
    cursor.execute(update_query, values)
    db.commit()
    
    return {'message': 'Item updated successfully'}

@app.route('/addcuti', methods=['POST'])
def addcuti():
    data = request.get_json()
    nik = data.get('nik')
    print(nik) 

    # cursor = db.cursor()
    # update_query = "UPDATE tblkaryawan SET nama_lengkap = %s, tempatlahir = %s , tgllahir = %s, agama = %s, alamat = %s, nohp = %s, golongandarah = %s, status = %s, photo = %s WHERE nik = %s"
    # values = (updated_data['nama_lengkap'], updated_data['tempatlahir'],updated_data['tgllahir'],updated_data['agama'],updated_data['alamat'],updated_data['nohp'],updated_data['golongandarah'],updated_data['status'],updated_data['photo'], updated_data['nik'])
    # print(update_query, values)
    # cursor.execute(update_query, values)
    # db.commit()
    
    # return {'message': 'Item updated successfully'}
    return jsonify({'message': 'Cuti added successfully'})




# Get all items
@app.route('/items', methods=['GET'])
def get_items():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tbluser")
    result = cursor.fetchone()
    if result:
        item = Item(result[0], result[1])
        return jsonify(item.__dict__)
    else:
        return jsonify({'error': 'Item not found'})

# Get item by id
@app.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tbluser WHERE id=%s", (id,))
    result = cursor.fetchone()
    if result:
        item = Item(result[0], result[1])
        return jsonify(item.__dict__)
    else:
        return jsonify({'error': 'Item not found'})

# Add new item
@app.route('/items', methods=['POST'])
def add_item():
    name = request.json['name']
    cursor = db.cursor()
    cursor.execute("INSERT INTO tbluser (username) VALUES (%s)", (name,))
    db.commit()
    return jsonify({'message': 'Item added successfully'})

# Delete item by id
@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM tbluser WHERE id=%s", (id,))
    db.commit()
    return jsonify({'message': 'Item deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)