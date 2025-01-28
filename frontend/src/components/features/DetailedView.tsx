import React from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/common/ui';
import { Badge } from '@/components/common/ui';
import { Calendar, Activity } from 'lucide-react';
import { formatDate, getTimeAgo } from '@/utils/date';
import type { Legislation } from '@/types/legislation';

interface DetailedViewProps {
  legislation: Legislation;
  isOpen: boolean;
  onClose: () => void;
}

export const DetailedView: React.FC<DetailedViewProps> = ({
  legislation,
  isOpen,
  onClose
}) => {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>{legislation.title}</DialogTitle>
        </DialogHeader>

        <div className="mt-4 space-y-4">
          <div className="flex flex-wrap gap-2">
            <Badge variant={legislation.status === 'active' ? 'success' : 'secondary'}>
              {legislation.status}
            </Badge>
            <Badge variant="outline">{legislation.type}</Badge>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {legislation.introduced_date && (
              <div className="flex items-center gap-2">
                <Calendar className="w-4 h-4" />
                <span>Introduced: {formatDate(legislation.introduced_date)}</span>
              </div>
            )}
            {legislation.last_action_date && (
              <div className="flex items-center gap-2">
                <Activity className="w-4 h-4" />
                <span>Last Action: {getTimeAgo(legislation.last_action_date)}</span>
              </div>
            )}
          </div>

          {legislation.summary && (
            <div className="prose max-w-none">
              <h3>Summary</h3>
              <p>{legislation.summary}</p>
            </div>
          )}

          {legislation.source_url && (
            <div className="mt-4">
              <a
                href={legislation.source_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline"
              >
                View Source
              </a>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
};
