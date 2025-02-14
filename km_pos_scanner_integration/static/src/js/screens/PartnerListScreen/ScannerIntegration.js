odoo.define('km_pos_scanner_integration.ScannerIntegration', function (require) {
    'use strict';

    const PartnerDetailsEdit = require('point_of_sale.PartnerDetailsEdit');
    const Registries = require('point_of_sale.Registries');
    const { useBarcodeReader } = require('point_of_sale.custom_hooks');
    var time = require('web.time');

    const { useState } = owl;

    const ScannerIntegration = PartnerDetailsEdit =>
        class extends PartnerDetailsEdit {
            setup() {
                super.setup();
                useBarcodeReader({
                    passport: this._barcodePassportAction
                });

                const partner = this.props.partner;
                this.changes = useState({
                    name: partner.name || "",
                    street: partner.street || "",
                    city: partner.city || "",
                    zip: partner.zip || "",
                    state_id: partner.state_id && partner.state_id[0],
                    country_id: partner.country_id && partner.country_id[0],
                    lang: partner.lang || "",
                    email: partner.email || "",
                    phone: partner.phone || "",
                    mobile: partner.mobile || "",
                    barcode: partner.barcode || "",
                    vat: partner.vat || "",
                    property_product_pricelist: this.getDefaultPricelist(partner),

                    surname: partner.surname || "",
                    forenames: partner.forenames || "",
                    flight_number: partner.flight_number || "",
                    flight_date: partner.flight_date || this.getTodayDate(),
                    date_of_birth: partner.date_of_birth || "",
                    expiry_date: partner.expiry_date || "",
                    issue_date: partner.issue_date || "",
                    document: partner.document || "",
                    doc_number: partner.doc_number || "",
                    issuing_state: partner.issuing_state || "",
                    nationality: partner.nationality || "",
                    height: partner.height || "",
                    weight: partner.weight || "",
                    hair_color: partner.hair_color || "",
                    eye_color: partner.eye_color || "",
                    gender: partner.gender || ""
                });
            }

            _barcodePassportAction(code) {
                var partner = this.changes;
                if (code.code.includes('Surname')) {
                    var result = code.code.substring(code.code.indexOf(':')+1,);
                    partner['name'] = result;
                    partner['surname'] = result;
                }
                if (code.code.includes('Forenames')) {
                    var result = code.code.substring(code.code.indexOf(':')+1,);
                    partner['forenames'] = result;
                }
                if (code.code.includes('Date of Birth')) {
                    var result = code.code.substring(code.code.indexOf(':')+1,);
                    partner['date_of_birth'] = result;
                }
                if (code.code.includes('Expiry Date')) {
                    var result = code.code.substring(code.code.indexOf(':')+1,);
                    partner['expiry_date'] = result;
                }
                if (code.code.includes('Issue Date')) {
                    var result = code.code.substring(code.code.indexOf(':')+1,);
                    partner['issue_date'] = result;
                }
                if (code.code.includes('Document')) {
                    var result = code.code.substring(code.code.indexOf(':')+1,);
                    partner['document'] = result;
                }
                if (code.code.includes('Doc. Number')) {
                    var result = code.code.substring(code.code.indexOf(':')+1,);
                    partner['doc_number'] = result;
                }
                if (code.code.includes('Issuing State')) {
                    var result = code.code.substring(code.code.indexOf(':')+1,);
                    partner['issuing_state'] = result;
                }
                if (code.code.includes('Nationality')) {
                    var result = code.code.substring(code.code.indexOf(':')+1,);
                    partner['nationality'] = result;
                }
                if (code.code.includes('Height')) {
                    var result = code.code.substring(code.code.indexOf(':')+1,);
                    partner['height'] = result;
                }
                if (code.code.includes('Weight')) {
                    var result = code.code.substring(code.code.indexOf(':')+1,);
                    partner['weight'] = result;
                }
                if (code.code.includes('Hair Color')) {
                    var result = code.code.substring(code.code.indexOf(':')+1,);
                    partner['hair_color'] = result;
                }
                if (code.code.includes('Eye Color')) {
                    var result = code.code.substring(code.code.indexOf(':')+1,);
                    partner['eye_color'] = result;
                }
                if (code.code.includes('Sex')) {
                    var result = code.code.substring(code.code.indexOf(':')+1,);
                    if (result.includes('M')) {
                        partner['gender'] = 'male';
                    } else if (result.includes('F')) {
                        partner['gender'] = 'female';
                    } else if (result.includes('X')) {
                        partner['gender'] = 'other';
                    }
                }
                this.props.partner = partner;
                this.render(true);
            }

            getTodayDate() {
                return time.date_to_str(new Date());
            }   
        };

    Registries.Component.extend(PartnerDetailsEdit, ScannerIntegration);

    return PartnerDetailsEdit;
});