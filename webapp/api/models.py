import datetime
from ..util.model_to_dict import Model
from ..import db

class Doc(Model):
    __tablename__ = 'doc'
    id= db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    dated = db.Column(db.DateTime(), default=datetime.datetime.now)
    template = db.Column(db.String(255), nullable=True)
    bkg_no = db.Column(db.String(255), nullable=True)
    shipper = db.Column(db.String(255), nullable=True)
    consignee = db.Column(db.String(255), nullable=True)
    notify = db.Column(db.String(255), nullable=True)
    also_notify = db.Column(db.String(255), nullable=True)
    vessel = db.Column(db.String(255), nullable=True)
    voyage = db.Column(db.String(255), nullable=True)
    place_of_receipt = db.Column(db.String(255), nullable=True)
    port_of_loading = db.Column(db.String(255), nullable=True)
    port_of_discharge = db.Column(db.String(255), nullable=True)
    place_of_delivery = db.Column(db.String(255), nullable=True)
    final_destination = db.Column(db.String(255), nullable=True)
    total_mark = db.Column(db.String(255), nullable=True)

    total_type = db.Column(db.String(255), nullable=True)
    total_packages = db.Column(db.String(255), nullable=True)
    description_of_goods = db.Column(db.String(255), nullable=True)
    total_weight = db.Column(db.String(255), nullable=True)
    total_measurement = db.Column(db.String(255), nullable=True)
    hs_code = db.Column(db.String(255), nullable=True)
    ams_scac_code = db.Column(db.String(255), nullable=True)
    aci_code = db.Column(db.String(255), nullable=True)
    bl_type = db.Column(db.String(255), nullable=True)
    payment = db.Column(db.String(255), nullable=True)
    containerdetail = db.relationship('ContainerDetail', backref="doc",uselist=False)
    def __repr__(self):
        return self.bkg_no if self.bkg_no is not None else 'Empty'


class ContainerDetail(Model):
    __tablename__ = 'containerdetail'
    id = db.Column(db.Integer(), primary_key=True)
    container_no = db.Column(db.String(255))
    seal_no = db.Column(db.String(255), nullable=True)
    container_type = db.Column(db.String(255), nullable=True)
    packages = db.Column(db.String(255), nullable=True)
    container_mark = db.Column(db.String(255), nullable=True)
    container_weight = db.Column(db.String(255), nullable=True)
    container_cbm = db.Column(db.String(255), nullable=True)
    doc_id = db.Column(db.Integer(), db.ForeignKey('doc.id'))
    
    def __repr__(self):
        return "<ContainerNo '{}'>".format(self.container_no)

#===========================================================================================================
# class Doc(models.Model):
#     name = models.CharField(max_length=250)
#     dated = models.DateTimeField(auto_now_add=True)
#     template = models.CharField(max_length=250, blank=True)

#     bkg_no = models.CharField(max_length=250, blank=True,
#                               verbose_name='Booking Number')
#     shipper = models.CharField(max_length=250, blank=True)
#     consignee = models.CharField(max_length=250, blank=True)
#     notify = models.CharField(max_length=250, blank=True)
#     also_notify = models.CharField(max_length=250, blank=True)
#     vessel = models.CharField(max_length=250, blank=True)
#     voyage = models.CharField(max_length=250, blank=True)
#     place_of_receipt = models.CharField(max_length=250, blank=True)
#     port_of_loading = models.CharField(max_length=250, blank=True)
#     port_of_discharge = models.CharField(max_length=250, blank=True)
#     place_of_delivery = models.CharField(max_length=250, blank=True)
#     final_destination = models.CharField(max_length=250, blank=True)
#     total_mark = models.CharField(max_length=250, blank=True)
#     total_type = models.CharField(max_length=250, blank=True)
#     total_packages = models.CharField(max_length=250, blank=True)
#     description_of_goods = models.CharField(max_length=250,
#                                             blank=True)
#     total_weight = models.CharField(max_length=250, blank=True)
#     total_cbm = models.CharField(max_length=250, blank=True)
#     hs_code = models.CharField(max_length=250, blank=True)
#     ams_scac_code = models.CharField(max_length=250, blank=True)
#     aci_code = models.CharField(max_length=250, blank=True)
#     bl_type = models.CharField(max_length=250, blank=True)
#     payment = models.CharField(max_length=250, blank=True)

#     def __str__(self):
#         return self.bkg_no if self.bkg_no is not None else 'Empty'


# class ContainerDetail(models.Model):
#     container_no = models.CharField(max_length=250,
#                                     verbose_name='Container Number')
#     seal_no = models.CharField(max_length=250, blank=True,
#                                verbose_name='Container Seal')
#     container_type = models.CharField(max_length=250, blank=True)
#     packages = models.CharField(max_length=250, blank=True)
#     container_mark = models.CharField(max_length=250, blank=True)
#     container_weight = models.CharField(max_length=250, blank=True)
#     container_cbm = models.CharField(max_length=250, blank=True)
#     doc = models.ForeignKey(
#         'Doc',
#         on_delete=models.CASCADE,
#         verbose_name='Booking Number'
#         )

#     def __str__(self):
#         return ''