# Frontend Integration Guide

## 🎯 Quick Start

You now have **4 new service files** ready to integrate with your React frontend:

1. ✅ `api.js` - Axios configuration
2. ✅ `organizationService.js` - Organization API calls
3. ✅ `fileService.js` - File upload handling
4. ✅ `organizationIntegration.js` - Integration helpers

---

## 📝 How to Use in OrganizationDetails.jsx

### **Step 1: Import Services**

Add these imports at the top of `OrganizationDetails.jsx`:

```javascript
import { organizationService } from '../../services/organizationService';
import { saveOrganizationStep, uploadFile } from '../../services/organizationIntegration';
```

---

### **Step 2: Add Organization ID State**

```javascript
const [organizationId, setOrganizationId] = useState(null);
const [loading, setLoading] = useState(false);
```

---

### **Step 3: Initialize Organization**

Add this useEffect to create or load organization:

```javascript
useEffect(() => {
  const initOrganization = async () => {
    // Check if we have a saved organization ID
    const savedId = localStorage.getItem('organizationId');
    
    if (savedId) {
      try {
        setLoading(true);
        const org = await organizationService.getOrganization(savedId);
        setOrganizationId(savedId);
        // Optionally load data into formData
        toast.success('Organization loaded!');
      } catch (error) {
        console.error('Failed to load organization:', error);
        localStorage.removeItem('organizationId');
      } finally {
        setLoading(false);
      }
    }
  };

  initOrganization();
}, []);
```

---

### **Step 4: Update File Upload Handler**

Replace the existing `handleFileUpload` function:

```javascript
const handleFileUpload = async (field, file) => {
  if (!file) return;
  
  // Validate file size and type (keep existing validation)
  const maxSize = field === 'labLogo' ? 1 * 1024 * 1024 : 2 * 1024 * 1024;
  if (file.size > maxSize) {
    toast.error(`File size should not exceed ${field === 'labLogo' ? '1MB' : '2MB'}`);
    return;
  }
  
  const allowedTypes = field === 'labLogo' 
    ? ['image/jpeg', 'image/jpg', 'image/png']
    : ['application/pdf'];
  
  if (!allowedTypes.includes(file.type)) {
    toast.error(`Please upload ${field === 'labLogo' ? 'JPG/PNG' : 'PDF'} files only`);
    return;
  }
  
  // Upload file to backend
  try {
    setLoading(true);
    const fileUrl = await uploadFile(file, field);
    handleInputChange(field, fileUrl);
    toast.success('File uploaded successfully!');
  } catch (error) {
    toast.error('File upload failed: ' + error.message);
  } finally {
    setLoading(false);
  }
};
```

---

### **Step 5: Update Save Handler**

Replace the existing `handleSave` function:

```javascript
const handleSave = async () => {
  if (!validateStep(currentStep)) return;
  
  try {
    setLoading(true);
    
    // Create organization if it doesn't exist (Step 1)
    if (!organizationId && currentStep === 1) {
      const newOrg = await organizationService.createOrganization({
        lab_name: formData.labName,
        lab_address: formData.labAddress,
        lab_state: formData.labState,
        lab_district: formData.labDistrict,
        lab_city: formData.labCity,
        lab_pin_code: formData.labPinCode,
      });
      
      setOrganizationId(newOrg.id);
      localStorage.setItem('organizationId', newOrg.id);
      toast.success('Organization created successfully!');
    } else if (organizationId) {
      // Update existing organization
      await saveOrganizationStep(organizationId, currentStep, formData);
      toast.success('Saved successfully!');
    } else {
      toast.error('Please complete Step 1 first');
      return;
    }
    
    // Move to next step
    if (currentStep < steps.length) {
      setCurrentStep(prev => prev + 1);
    }
  } catch (error) {
    toast.error('Save failed: ' + error.message);
    console.error('Save error:', error);
  } finally {
    setLoading(false);
  }
};
```

---

### **Step 6: Update Submit Handler**

Replace the existing `handleSubmit` function:

```javascript
const handleSubmit = async () => {
  if (!validateStep(currentStep)) return;
  
  if (!organizationId) {
    toast.error('Please save your data first');
    return;
  }
  
  try {
    setLoading(true);
    
    // Get checklist to verify completion
    const checklist = await organizationService.getChecklist(organizationId);
    
    if (!checklist.is_ready_for_submission) {
      toast.error('Please complete all required fields');
      return;
    }
    
    // Submit organization
    await organizationService.submitOrganization(organizationId);
    toast.success('Organization submitted successfully!');
    
    // Optionally redirect or show success page
    // navigate('/success');
  } catch (error) {
    toast.error('Submission failed: ' + error.message);
    console.error('Submit error:', error);
  } finally {
    setLoading(false);
  }
};
```

---

### **Step 7: Add Loading Indicator**

Add a loading overlay to your component:

```javascript
{loading && (
  <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div className="bg-white p-6 rounded-lg shadow-xl">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
      <p className="mt-4 text-gray-700">Processing...</p>
    </div>
  </div>
)}
```

---

## 🧪 Testing Steps

1. **Start Backend**: Make sure `uvicorn app.main:app --reload` is running
2. **Start Frontend**: Run your React app
3. **Test Flow**:
   - Fill in Step 1 (Laboratory Details)
   - Click "Save & Next"
   - Check browser console for API calls
   - Verify data saved in backend (check Swagger UI)
   - Upload a logo
   - Continue through all steps
   - Submit organization

---

## 🔍 Debugging

### Check API Calls in Browser Console

The services log all requests/responses:
```
🚀 API Request: POST /organizations
✅ API Response: /organizations 201
```

### Check Backend Logs

Your FastAPI terminal will show:
```
INFO:     127.0.0.1:xxxxx - "POST /api/v1/organizations HTTP/1.1" 201 Created
```

### Test API Directly

Use Swagger UI: http://localhost:8000/api/docs

---

## ⚙️ Environment Variables

Create `.env` in your frontend root:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_FILE_API_URL=http://localhost:8000/api/v1/files
```

---

## 🎯 Next Steps

1. ✅ Services created
2. ⏳ Update OrganizationDetails.jsx
3. ⏳ Test each step
4. ⏳ Handle edge cases
5. ⏳ Add proper error messages
6. ⏳ Implement loading states

---

## 📚 API Reference

### Organization Endpoints

- `POST /api/v1/organizations` - Create
- `GET /api/v1/organizations/{id}` - Get
- `PUT /api/v1/organizations/{id}/laboratory-details` - Step 1
- `PUT /api/v1/organizations/{id}/registered-office` - Step 2
- ... (all 11 steps)
- `GET /api/v1/organizations/{id}/checklist` - Validation
- `POST /api/v1/organizations/{id}/submit` - Submit

### File Endpoints

- `POST /api/v1/files/upload/logo` - Upload logo
- `POST /api/v1/files/upload/document` - Upload document
- `DELETE /api/v1/files/delete` - Delete file

---

## 💡 Tips

- Always check `organizationId` exists before saving
- Handle errors gracefully with toast notifications
- Show loading states during API calls
- Validate data before sending to backend
- Store `organizationId` in localStorage for persistence
- Clear localStorage on logout

---

**Ready to integrate!** 🚀

Start by updating your `OrganizationDetails.jsx` component with the code above.
