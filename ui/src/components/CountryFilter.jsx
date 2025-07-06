import { useQuery, gql } from '@apollo/client';
import { Text, Spinner, Card, Dropdown, Option } from '@fluentui/react-components';
import { useState } from 'react';

const GET_CUSTOMER_COUNTRIES = gql`
  query GetCustomerCountries {
    customer {
      Country
      _distinct_ {
        CustomerId
      }
    }
  }
`;

export const CountryFilter = () => {
  const { loading, error, data } = useQuery(GET_CUSTOMER_COUNTRIES);
  const [selectedCountry, setSelectedCountry] = useState('');

  if (loading) {
    return (
      <Card className="p-4">
        <div className="flex items-center gap-2">
          <Spinner size="small" />
          <Text>Loading countries...</Text>
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="p-4">
        <Text className="text-red-600">Error loading countries: {error.message}</Text>
      </Card>
    );
  }

  const countries = data?.customer || [];

  const handleCountryChange = (event, data) => {
    setSelectedCountry(data.optionValue);
  };

  return (
    <Card className="p-4">
      <div className="space-y-4">
        <Text size={500} weight="semibold" className="text-gray-800">
          Customer Countries
        </Text>
        
        {countries.length > 0 ? (
          <Dropdown
            placeholder="Select a country..."
            value={selectedCountry}
            onOptionSelect={handleCountryChange}
            className="w-full"
            clearable={true}
          >
            {countries.map((item, index) => (
              <Option key={index} text={item.Country}>
                <div className="flex justify-between items-center w-full">
                  <span>{item.Country}</span>
                  <span className="font-semibold text-blue-600 ml-2">
                    {item._distinct_?.CustomerId || 0} customers
                  </span>
                </div>
              </Option>
            ))}
          </Dropdown>
        ) : (
          <Text className="text-gray-500 text-center py-4">
            No country data available
          </Text>
        )}
        
        {selectedCountry && (
          <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-md">
            <Text className="text-blue-800">
              Selected: <strong>{selectedCountry}</strong>
            </Text>
          </div>
        )}
      </div>
    </Card>
  );
};

/*
                
*/