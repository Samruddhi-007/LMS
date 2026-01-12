/**
 * Organization Service
 * API calls for organization management (all 11 steps)
 */
import api from './api';

export const organizationService = {
    /**
     * Create a new organization
     */
    async createOrganization(data) {
        return await api.post('/organizations', data);
    },

    /**
     * Get organization by ID
     */
    async getOrganization(id) {
        return await api.get(`/organizations/${id}`);
    },

    /**
     * Get all organizations (with pagination)
     */
    async getOrganizations(skip = 0, limit = 100) {
        return await api.get('/organizations', { params: { skip, limit } });
    },

    /**
     * Delete organization
     */
    async deleteOrganization(id) {
        return await api.delete(`/organizations/${id}`);
    },

    // ========================================================================
    // Step-wise Updates
    // ========================================================================

    /**
     * Step 1: Update Laboratory Details
     */
    async updateLaboratoryDetails(id, data) {
        return await api.put(`/organizations/${id}/laboratory-details`, data);
    },

    /**
     * Step 2: Update Registered Office & Top Management
     */
    async updateRegisteredOffice(id, data) {
        return await api.put(`/organizations/${id}/registered-office`, data);
    },

    /**
     * Step 3: Update Parent Organization
     */
    async updateParentOrganization(id, data) {
        return await api.put(`/organizations/${id}/parent-organization`, data);
    },

    /**
     * Step 3: Update Bank Details
     */
    async updateBankDetails(id, data) {
        return await api.put(`/organizations/${id}/bank-details`, data);
    },

    /**
     * Step 4: Update Working Schedule & Shift Timings
     */
    async updateWorkingSchedule(id, data) {
        return await api.put(`/organizations/${id}/working-schedule`, data);
    },

    /**
     * Step 5: Update Compliance Documents
     */
    async updateComplianceDocuments(id, data) {
        return await api.put(`/organizations/${id}/compliance-documents`, data);
    },

    /**
     * Step 6: Update Policy Documents
     */
    async updatePolicyDocuments(id, data) {
        return await api.put(`/organizations/${id}/policy-documents`, data);
    },

    /**
     * Step 7: Update Infrastructure Details
     */
    async updateInfrastructure(id, data) {
        return await api.put(`/organizations/${id}/infrastructure`, data);
    },

    /**
     * Step 8: Update Accreditation Documents
     */
    async updateAccreditation(id, data) {
        return await api.put(`/organizations/${id}/accreditation`, data);
    },

    /**
     * Step 8: Update Other Lab Details
     */
    async updateOtherDetails(id, data) {
        return await api.put(`/organizations/${id}/other-details`, data);
    },

    /**
     * Step 9: Update Quality Manual & SOPs
     */
    async updateQualityManual(id, data) {
        return await api.put(`/organizations/${id}/quality-manual`, data);
    },

    /**
     * Step 10: Update Quality Formats & Procedures
     */
    async updateQualityFormats(id, data) {
        return await api.put(`/organizations/${id}/quality-formats`, data);
    },

    // ========================================================================
    // Validation & Submission
    // ========================================================================

    /**
     * Get validation checklist
     */
    async getChecklist(id) {
        return await api.get(`/organizations/${id}/checklist`);
    },

    /**
     * Submit organization for approval
     */
    async submitOrganization(id) {
        return await api.post(`/organizations/${id}/submit`);
    },
};

export default organizationService;
