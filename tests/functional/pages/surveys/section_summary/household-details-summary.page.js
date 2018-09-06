// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class HouseholdDetailsSummaryPage extends QuestionPage {

  constructor() {
    super('household-details-summary');
  }

  insuranceTypeAnswer() { return '#insurance-type-answer-answer'; }

  insuranceTypeAnswerEdit() { return '[data-qa="insurance-type-answer-edit"]'; }

  insuranceAddressAnswer() { return '#insurance-address-answer-answer'; }

  insuranceAddressAnswerEdit() { return '[data-qa="insurance-address-answer-edit"]'; }

  propertyDetailsTitle() { return '#property-details'; }

  addressDurationAnswer() { return '#address-duration-answer-answer'; }

  addressDurationAnswerEdit() { return '[data-qa="address-duration-answer-edit"]'; }

  addressLengthTitle() { return '#address-length'; }

  propertyDetailsSummaryGroupTitle() { return '#property-details-summary-group'; }

  houseTypeAnswer() { return '#house-type-answer-answer'; }

  houseTypeAnswerEdit() { return '[data-qa="house-type-answer-edit"]'; }

  houseDetailsTitle() { return '#house-details'; }

  householdDetailsSummaryGroupTitle() { return '#household-details-summary-group'; }

  lastName() { return '#last-name-answer'; }

  lastNameEdit() { return '[data-qa="last-name-edit"]'; }

  multipleQuestionsGroupTitle() { return '#multiple-questions-group'; }

  summaryGroupTitle() { return '#summary-group'; }

}
module.exports = new HouseholdDetailsSummaryPage();
