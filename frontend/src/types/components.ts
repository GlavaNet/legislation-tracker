import { ComponentPropsWithoutRef, ElementType } from 'react';

export type PolymorphicRef<C extends ElementType> = 
  ComponentPropsWithoutRef<C>['ref'];

export type PolymorphicComponentProps<
  C extends ElementType,
  Props = {}
> = {
  as?: C;
} & ComponentPropsWithoutRef<C> &
  Props;
