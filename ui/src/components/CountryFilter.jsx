import { useQuery, gql } from '@apollo/client';
import { Text, Spinner, Card } from '@fluentui/react-components';

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

  return (
    <Card className="p-4">
      <div className="space-y-4">
        <Text size={500} weight="semibold" className="text-gray-800">
          Customer Countries
        </Text>
        
        <div className="space-y-2">
          {countries.map((item, index) => (
            <div key={index} className="flex justify-between items-center p-2 bg-gray-50 rounded-md">
              <Text className="text-gray-700">{item.Country}</Text>
              <Text className="font-semibold text-blue-600">
                {item._distinct_?.CustomerId || 0} customers
              </Text>
            </div>
          ))}
        </div>
        
        {countries.length === 0 && (
          <Text className="text-gray-500 text-center py-4">
            No country data available
          </Text>
        )}
      </div>
    </Card>
  );
};