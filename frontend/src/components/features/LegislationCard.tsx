interface LegislationCardProps {
  legislation: Legislation;
}

export const LegislationCard: React.FC<LegislationCardProps> = ({ legislation }) => {
  return (
    <Card className="p-4">
      <h2 className="text-lg font-semibold">{legislation.title}</h2>
      {legislation.summary && (
        <p className="mt-2 text-gray-600">{legislation.summary}</p>
      )}
      <div className="mt-4 flex items-center gap-2">
        {legislation.status && (
          <Badge variant="outline">{legislation.status}</Badge>
        )}
        {legislation.introduced_date && (
          <span className="text-sm text-gray-500">
            Introduced: {formatDate(legislation.introduced_date)}
          </span>
        )}
      </div>
    </Card>
  );
};
