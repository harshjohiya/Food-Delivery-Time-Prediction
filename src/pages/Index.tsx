import { useState } from "react";
import { Loader2, Clock, Utensils, AlertCircle, CheckCircle } from "lucide-react";

interface FormData {
  deliveryPersonAge: string;
  deliveryPersonRating: string;
  restaurantLatitude: string;
  restaurantLongitude: string;
  deliveryLatitude: string;
  deliveryLongitude: string;
  typeOfOrder: string;
  typeOfVehicle: string;
}

// Configure API URL - can be overridden with environment variable
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/predict";

const Index = () => {
  const [formData, setFormData] = useState<FormData>({
    deliveryPersonAge: "",
    deliveryPersonRating: "",
    restaurantLatitude: "",
    restaurantLongitude: "",
    deliveryLatitude: "",
    deliveryLongitude: "",
    typeOfOrder: "",
    typeOfVehicle: "",
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<number | null>(null);
  const [distanceKm, setDistanceKm] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    setError(null);
  };

  const validateForm = (): boolean => {
    const requiredFields = Object.entries(formData);
    for (const [key, value] of requiredFields) {
      if (!value.trim()) {
        setError(`Please fill in all fields`);
        return false;
      }
    }

    const rating = parseFloat(formData.deliveryPersonRating);
    if (rating < 1 || rating > 5) {
      setError("Rating must be between 1 and 5");
      return false;
    }

    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setResult(null);
    setDistanceKm(null);

    if (!validateForm()) return;

    setLoading(true);

    try {
      const payload = {
        Delivery_person_Age: parseInt(formData.deliveryPersonAge),
        Delivery_person_Ratings: parseFloat(formData.deliveryPersonRating),
        Restaurant_latitude: parseFloat(formData.restaurantLatitude),
        Restaurant_longitude: parseFloat(formData.restaurantLongitude),
        Delivery_location_latitude: parseFloat(formData.deliveryLatitude),
        Delivery_location_longitude: parseFloat(formData.deliveryLongitude),
        Type_of_order: formData.typeOfOrder,
        Type_of_vehicle: formData.typeOfVehicle,
      };

      console.log("Sending request to:", API_URL);
      console.log("Payload:", payload);

      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        // Handle API error responses
        throw new Error(
          data.detail || `Server error: ${response.status} ${response.statusText}`
        );
      }

      console.log("Response:", data);
      
      setResult(data.predicted_delivery_time_minutes);
      if (data.distance_km) {
        setDistanceKm(data.distance_km);
      }
    } catch (err) {
      console.error("Prediction error:", err);
      
      if (err instanceof TypeError && err.message === "Failed to fetch") {
        setError(
          "Unable to connect to the server. Please ensure the backend is running on " + 
          API_URL.replace("/predict", "")
        );
      } else {
        setError(
          err instanceof Error ? err.message : "An unexpected error occurred"
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background py-8 px-4 sm:py-12">
      <div className="max-w-lg mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-primary/10 rounded-2xl mb-4">
            <Utensils className="w-8 h-8 text-primary" />
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-foreground">
            Food Delivery Time Predictor
          </h1>
          <p className="text-muted-foreground mt-2">
            Enter delivery details to get an estimated time
          </p>
        </div>

        {/* Form Card */}
        <div className="card-elevated p-6 sm:p-8">
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Delivery Person Details */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label htmlFor="deliveryPersonAge" className="label-text">
                  Delivery Person Age
                </label>
                <input
                  type="number"
                  id="deliveryPersonAge"
                  name="deliveryPersonAge"
                  value={formData.deliveryPersonAge}
                  onChange={handleChange}
                  placeholder="e.g., 25"
                  min="18"
                  max="65"
                  className="input-field"
                />
              </div>
              <div>
                <label htmlFor="deliveryPersonRating" className="label-text">
                  Delivery Person Rating
                </label>
                <input
                  type="number"
                  id="deliveryPersonRating"
                  name="deliveryPersonRating"
                  value={formData.deliveryPersonRating}
                  onChange={handleChange}
                  placeholder="1.0 - 5.0"
                  min="1"
                  max="5"
                  step="0.1"
                  className="input-field"
                />
              </div>
            </div>

            {/* Restaurant Location */}
            <div>
              <p className="label-text">Restaurant Location</p>
              <div className="grid grid-cols-2 gap-3">
                <input
                  type="number"
                  name="restaurantLatitude"
                  value={formData.restaurantLatitude}
                  onChange={handleChange}
                  placeholder="Latitude"
                  step="any"
                  className="input-field"
                />
                <input
                  type="number"
                  name="restaurantLongitude"
                  value={formData.restaurantLongitude}
                  onChange={handleChange}
                  placeholder="Longitude"
                  step="any"
                  className="input-field"
                />
              </div>
            </div>

            {/* Delivery Location */}
            <div>
              <p className="label-text">Delivery Location</p>
              <div className="grid grid-cols-2 gap-3">
                <input
                  type="number"
                  name="deliveryLatitude"
                  value={formData.deliveryLatitude}
                  onChange={handleChange}
                  placeholder="Latitude"
                  step="any"
                  className="input-field"
                />
                <input
                  type="number"
                  name="deliveryLongitude"
                  value={formData.deliveryLongitude}
                  onChange={handleChange}
                  placeholder="Longitude"
                  step="any"
                  className="input-field"
                />
              </div>
            </div>

            {/* Dropdowns */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label htmlFor="typeOfOrder" className="label-text">
                  Type of Order
                </label>
                <select
                  id="typeOfOrder"
                  name="typeOfOrder"
                  value={formData.typeOfOrder}
                  onChange={handleChange}
                  className="select-field"
                >
                  <option value="">Select order type</option>
                  <option value="Snack">Snack</option>
                  <option value="Meal">Meal</option>
                  <option value="Drinks">Drinks</option>
                  <option value="Buffet">Buffet</option>
                </select>
              </div>
              <div>
                <label htmlFor="typeOfVehicle" className="label-text">
                  Type of Vehicle
                </label>
                <select
                  id="typeOfVehicle"
                  name="typeOfVehicle"
                  value={formData.typeOfVehicle}
                  onChange={handleChange}
                  className="select-field"
                >
                  <option value="">Select vehicle</option>
                  <option value="motorcycle">Motorcycle</option>
                  <option value="scooter">Scooter</option>
                  <option value="bicycle">Bicycle</option>
                </select>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="btn-primary flex items-center justify-center gap-2 mt-6"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Predicting...
                </>
              ) : (
                "Predict Delivery Time"
              )}
            </button>
          </form>

          {/* Result Display */}
          {result !== null && (
            <div className="result-card mt-6">
              <div className="flex items-center justify-center gap-2 mb-3">
                <CheckCircle className="w-6 h-6 text-green-500" />
                <Clock className="w-8 h-8 text-primary" />
              </div>
              <p className="text-muted-foreground text-sm mb-1">
                Estimated Delivery Time
              </p>
              <p className="text-3xl font-bold text-foreground">
                {Math.round(result)}{" "}
                <span className="text-lg font-medium text-muted-foreground">
                  minutes
                </span>
              </p>
              {distanceKm !== null && (
                <p className="text-sm text-muted-foreground mt-2">
                  Distance: {distanceKm.toFixed(2)} km
                </p>
              )}
            </div>
          )}

          {/* Error Display */}
          {error && (
            <div className="error-card mt-6">
              <div className="flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="font-medium">{error}</p>
                  <p className="text-sm mt-1 opacity-90">
                    Please check your inputs and try again.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer Note */}
        <p className="text-center text-muted-foreground text-sm mt-6">
          Predictions are estimates based on historical data
        </p>
      </div>
    </div>
  );
};

export default Index;
