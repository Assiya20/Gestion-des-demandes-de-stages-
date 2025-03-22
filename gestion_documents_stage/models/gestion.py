from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Request(models.Model):
    _name = 'gestion_documents_stage.request'
    _description = 'Demande de Stage'

    # Informations de l'étudiant
    name = fields.Char(string="Nom de l'Étudiant", required=True, tracking=True)
    email = fields.Char(string="Email", required=True)
    cne = fields.Char(string="CNE", required=True)
    genre = fields.Selection([
        ('male', 'Homme'),
        ('female', 'Femme')
    ], string="Genre", required=True)
    niveau = fields.Selection([
        ('1a', 'Première année du cycle d’ingénieur'),
        ('2a', 'Deuxième année du cycle d’ingénieur'),
        ('3a', 'Troisième année du cycle d’ingénieur'),
    ], string="Niveau", required=True)

    specialite = fields.Selection([
        ('itrc', 'Ingénierie des Technologies de l’Information et Réseaux de Communication'),
        ('dscc', 'Ingénierie Data Sciences et Cloud Computing'),
        ('gc', 'Génie Civil'),
        ('ge', 'Génie Électrique'),
        ('gi', 'Génie Industriel'),
        ('ginf', 'Génie Informatique'),
        ('gseir', 'Génie des Systèmes Électronique, Informatique et Réseaux'),
        ('sic', 'Sécurité Informatique et Cyber Sécurité'),
        ('mgsi', 'Management et Gouvernance des Systèmes d’Information'),
    ], string="Spécialité", required=True)
    annee_universitaire = fields.Char(string="Année Universitaire", required=True)
    # Informations de l'entreprise
    entreprise = fields.Char(string="Entreprise d'accueil", required=True)
    adresse_entreprise = fields.Char(string="Adresse de l’Entreprise", required=True)
    ville_entreprise = fields.Char(string="Ville de l’Entreprise", required=True)
    telephone_entreprise = fields.Char(string="Téléphone / Fax de l’Entreprise", required=True)
    tuteur_entreprise = fields.Char(string="Tuteur en Entreprise", required=True)
    tuteur_academique = fields.Char(string="Tuteur Académique", required=True)

            # Dates du stage
    date_debut = fields.Date(string="Date de Début", required=True)
    date_fin = fields.Date(string="Date de Fin", required=True)
    # Statut de la demande
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('submitted', 'Soumis'),
        ('validated', 'Validé'),
        ('rejected', 'Rejeté'),
        ('signed', 'Signé')
    ], string="Statut", default='draft', tracking=True)

    document_ids = fields.One2many('gestion_documents_stage.document', 'request_id', string="Documents de Stage")

    # Exemplaires des documents de stage
    document_demande = fields.Binary(string="Exemplaire Demande de Stage")
    document_convention = fields.Binary(string="Exemplaire Convention de Stage")
    document_fiche = fields.Binary(string="Exemplaire Fiche de Stage")



    # Actions pour changer l’état de la demande
    def action_submit(self):
        self.state = 'submitted'

    def action_validate(self):
        self.state = 'validated'

    def action_reject(self):
        self.state = 'rejected'

    def action_sign(self):
        self.state = 'signed'

    # Action pour télécharger le fichier 'Demande de Stage'
    def action_download_demande(self):
        if not self.document_demande:
            raise ValidationError("Le document 'Demande de Stage' n'a pas été téléchargé.")
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{self._name},{self.id},document_demande?download=true',
            'target': 'new'
        }

    # Action pour télécharger le fichier 'Convention de Stage'
    def action_download_convention(self):
        if not self.document_convention:
            raise ValidationError("Le document 'Convention de Stage' n'a pas été téléchargé.")
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{self._name},{self.id},document_convention?download=true',
            'target': 'new'
        }

    # Action pour télécharger le fichier 'Fiche de Stage'

    def action_download_fiche(self):
        if not self.document_fiche:
            raise ValidationError("Le document 'Fiche de Stage' n'a pas été téléchargé.")
        return {
        'type': 'ir.actions.act_url',
        'url': f'/web/content/{self._name}/{self.id}/document_fiche?download=true',
        'target': 'new',
    }
    def action_submit_documents(self):
        if not self.document_ids:
            raise ValidationError("Veuillez télécharger au moins un document.")
        self.state = 'submitted'
        # Méthode pour accepter les documents
    def action_accept_documents(self):
        for record in self:
            # Accepter tous les documents liés et changer leur état
            for document in record.document_ids:
                if document.state == 'draft':
                    document.state = 'validated'
            record.state = 'validated'  # Changer l’état global de la demande
        return {
                    'effect': {
                    'fadeout': 'slow',
                    'message': "Les documents ont été acceptés avec succès.",
                    'type': 'rainbow_man',
                    },
                    'type': 'ir.actions.client',
                    'tag': 'reload',
        }

    def action_reject_documents(self):
        for record in self:
            # Rejeter tous les documents liés et changer l'état de la demande
            record.state = 'rejected'  # Change l’état global de la demande
        return {
            'effect': {
                'fadeout': 'slow',
                'message': "Les documents ont été rejetés. Veuillez les resoumettre.",
                'type': 'rainbow_man',
            },
            'reload': True
        }


    # Vérification des dates
    @api.constrains('date_debut', 'date_fin')
    def _check_dates(self):
        for record in self:
            if record.date_debut and record.date_fin and record.date_debut >= record.date_fin:
                raise ValidationError("La date de début doit être avant la date de fin.")

class Document(models.Model):
    _name = 'gestion_documents_stage.document'
    _description = 'Document de Stage'

    name = fields.Char(string="Nom du Document", required=True)
    document_type = fields.Selection([
        ('demande', 'Demande de Stage'),
        ('convention', 'Convention de Stage'),
        ('fiche', 'Fiche de Stage')
    ], string="Type de Document", required=True)
    file = fields.Binary(string="Fichier", required=True)
    request_id = fields.Many2one('gestion_documents_stage.request', string="Demande de Stage", ondelete="cascade")
    signature = fields.Binary(string="Signature", attachment=True)

    state = fields.Selection([
        ('draft', 'Brouillon'),
            ('validated', 'Validé'),  # ✅ Ajout de l'état "Validé"
        ('signed', 'Signé')
    ], string="Statut", default='draft', tracking=True)
   
    

    def action_sign(self):
        for record in self:
            if not record.signature:
                raise ValidationError("Veuillez ajouter une signature avant de valider.")
            if record.state == 'signed':
                raise ValidationError("Ce document est déjà signé.")
            record.state = 'signed'

        return {
            'effect': {
                'fadeout': 'slow',
                'message': "🎉 Le document a été signé avec succès !",
                'type': 'rainbow_man',
            }
        }


class Signature(models.Model):
    _name = 'gestion_documents_stage.signature'
    _description = 'Signature des Documents'

    request_id = fields.Many2one('gestion_documents_stage.request', string="Demande de Stage", ondelete="cascade")
    signed_by = fields.Many2one('res.users', string="Signé par", default=lambda self: self.env.user)
    signed_date = fields.Datetime(string="Date de Signature", default=fields.Datetime.now)
    document_id = fields.Many2one('gestion_documents_stage.document', string="Document Signé")
    signature = fields.Binary(string="Signature", attachment=True)

    @api.constrains('signature')
    def _check_signature(self):
        for record in self:
            if not record.signature:
                raise ValidationError("La signature électronique est obligatoire pour cette action.")
