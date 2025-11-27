# Brand Feature Documentation

## Overview
The Brand feature has been successfully added to the backend to manage product brands with logos and centralized brand information.

## Database Structure

### Brand Model
Located in `shop/models.py`

**Fields:**
- `name`: CharField(200) - Nom de la marque (unique)
- `slug`: SlugField(200) - URL slug (unique, auto-generated from name)
- `logo`: ImageField - Logo de la marque (upload to 'brands/')
- `description`: TextField - Description de la marque
- `website`: URLField - Site web de la marque
- `order`: IntegerField - Ordre d'affichage (default: 0)
- `is_active`: BooleanField - Marque active (default: True)
- `created_at`: DateTimeField - Date de création
- `updated_at`: DateTimeField - Date de modification

**Relationships:**
- One-to-Many with Product: `brand` ForeignKey in Product model
- Related name: `products` (accessible via `brand.products.all()`)

### Product Model Updates
- Added `brand` ForeignKey to Brand (nullable, SET_NULL on delete)
- Kept `brand_text` CharField for backward compatibility (deprecated)

## Migrations Applied

1. **0004_rename_brand_to_brand_text** (Faked)
   - Created Brand table
   - Renamed original brand CharField to brand_text

2. **0005_add_brand_foreign_key**
   - Added brand ForeignKey to Product model

## API Endpoints

### Brand Endpoints

**List All Brands**
```
GET /api/brands/
```
Returns all active brands with:
- id, name, slug
- logo_url (absolute URL)
- description, website
- product_count (number of products)
- order, created_at, updated_at

**Get Brand Details**
```
GET /api/brands/{slug}/
```
Returns specific brand details with same fields

### Product Endpoints Updates

Product list and detail endpoints now include:
- `brand_name`: String - Name of the brand (from brand.name)
- `brand_logo_url`: String - Absolute URL to brand logo image (null if no logo)
- `brand_data`: Object (detail view only) - Full brand information
  ```json
  {
    "id": 1,
    "name": "ASUS",
    "slug": "asus",
    "logo_url": "http://localhost:8000/media/brands/asus.png",
    "product_count": 15
  }
  ```

## Admin Interface

### BrandAdmin
- **List Display**: name, order, is_active, website, created_at
- **Filters**: is_active
- **Search**: name, description
- **Slug**: Auto-populated from name
- **Fieldsets**:
  - Informations de base: name, slug, logo
  - Description: description, website
  - Paramètres: order, is_active

### ProductAdmin Updates
- **List Display**: Added brand column
- **List Filter**: Added brand filter
- **Fieldsets**: Added brand in Classification section

## Serializers

### BrandSerializer
Located in `shop/serializers.py`

**Fields:**
- All model fields
- `logo_url`: SerializerMethodField - Absolute URL to logo
- `product_count`: SerializerMethodField - Count of related products

### ProductListSerializer Updates
Added fields:
- `brand_name`: CharField(source='brand.name')
- `brand_logo_url`: SerializerMethodField

### ProductDetailSerializer Updates
Added field:
- `brand_data`: SerializerMethodField - Returns full BrandSerializer data

## Usage Examples

### Creating a Brand (Django Admin)
1. Navigate to Admin Panel → Shop → Brands
2. Click "Add Brand"
3. Fill in:
   - Name: "ASUS"
   - Logo: Upload image file
   - Description: "Leading computer hardware manufacturer"
   - Website: "https://www.asus.com"
   - Order: 1
   - Active: ✓
4. Save

### Assigning Brand to Product (Django Admin)
1. Navigate to Admin Panel → Shop → Products
2. Edit or create a product
3. In Classification section:
   - Select brand from dropdown
4. Save

### Fetching Brands via API
```bash
# Get all brands
curl http://localhost:8000/api/brands/

# Get specific brand
curl http://localhost:8000/api/brands/asus/

# Get products filtered by brand
curl http://localhost:8000/api/products/?brand=asus
```

## Frontend Integration (Next Steps)

### Update TypeScript Types
In `e-commece/lib/types.ts`, update Product interface:
```typescript
export interface Brand {
  id: number;
  name: string;
  slug: string;
  logo_url: string | null;
  product_count: number;
}

export interface Product {
  // ... existing fields
  brand_name: string;
  brand_logo_url: string | null;
  brand_data?: Brand;  // Available in detail view
}
```

### Add API Functions
In `e-commece/lib/api.ts`:
```typescript
export async function getBrands(): Promise<Brand[]> {
  const response = await fetch(`${API_URL}/brands/`);
  return response.json();
}
```

### Display Brand Logo in Components
```tsx
{product.brand_logo_url && (
  <img 
    src={product.brand_logo_url} 
    alt={product.brand_name}
    className="h-6 w-auto"
  />
)}
```

## Data Migration Strategy

To migrate existing `brand_text` data to Brand model:
1. Extract unique brand names: `Product.objects.values_list('brand_text', flat=True).distinct()`
2. Create Brand objects for each unique name
3. Update Product.brand FK to reference new Brand objects
4. Keep brand_text for reference (marked as deprecated)

## Benefits

✅ **Centralized Brand Management**: All brand info in one place
✅ **Brand Logos**: Visual representation with images
✅ **Brand Filtering**: Easy filtering in admin and API
✅ **Consistency**: Standardized brand names across products
✅ **Analytics**: Track products per brand (product_count)
✅ **Flexibility**: Can add more brand attributes (country, rating, etc.)
✅ **Backward Compatible**: Old brand_text field preserved

## Testing

Run Django checks:
```bash
python manage.py check
```

Test API endpoints:
```bash
# Test brands endpoint
curl http://localhost:8000/api/brands/

# Test product with brand data
curl http://localhost:8000/api/products/
```

Access admin interface:
```
http://localhost:8000/admin-panel/
```

## Next Steps

1. ✅ Backend Brand model created
2. ✅ Migrations applied
3. ✅ Admin interface configured
4. ✅ API endpoints added
5. ✅ Serializers updated
6. ⏳ Update frontend types (types.ts)
7. ⏳ Add getBrands() function to api.ts
8. ⏳ Display brand logos in product cards
9. ⏳ Add brand filter to nouveautés/promo pages
10. ⏳ Create brand management page (admin)

## Files Modified

**Backend:**
- `shop/models.py` - Added Brand model, updated Product
- `shop/admin.py` - Added BrandAdmin, updated ProductAdmin
- `shop/serializers.py` - Added BrandSerializer, updated Product serializers
- `shop/views.py` - Added BrandViewSet
- `shop/urls.py` - Registered brands router
- `admin_panel/forms.py` - Updated ProductForm for brand_text
- Migrations: 0004 and 0005

**Frontend (Pending):**
- `lib/types.ts` - Add Brand interface
- `lib/api.ts` - Add getBrands function
- Product card components - Display brand logos

## Conclusion

The Brand feature is fully implemented in the backend and ready for frontend integration. All API endpoints are functional and tested. The system maintains backward compatibility while providing a modern, extensible brand management system.
